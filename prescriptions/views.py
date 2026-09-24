from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from authentication.permissions import doctor_required
from .models import Prescription, PrescriptionItem
from .forms import PrescriptionForm, PrescriptionItemFormSet
from .utils import render_to_pdf
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from consultations.models import Consultation

@login_required
@doctor_required
@transaction.atomic
def create_prescription(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient_id = request.GET.get('patient_id')
    consultation_id = request.GET.get('consultation_id')
    
    initial_data = {}
    if patient_id:
        initial_data['patient'] = get_object_or_404(PatientProfile, id=patient_id)
    if consultation_id:
        initial_data['consultation'] = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = doctor
            prescription.save()
            
            formset = PrescriptionItemFormSet(request.POST, instance=prescription)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Prescription created successfully.")
                return redirect('prescription_list')
            else:
                prescription.delete()  # Rollback if formset is invalid
                messages.error(request, "Error adding prescription medications. Please verify inputs.")
        else:
            messages.error(request, "Error creating prescription.")
    else:
        form = PrescriptionForm(initial=initial_data)
        formset = PrescriptionItemFormSet()
        
    return render(request, 'prescriptions/create_prescription.html', {
        'form': form,
        'formset': formset
    })

@login_required
def prescription_list(request):
    q = request.GET.get('q', '').strip()
    
    if request.user.role == 'patient':
        patient = get_object_or_404(PatientProfile, user=request.user)
        prescriptions = Prescription.objects.filter(patient=patient)
    elif request.user.role == 'doctor':
        doctor = get_object_or_404(DoctorProfile, user=request.user)
        prescriptions = Prescription.objects.filter(doctor=doctor)
    elif request.user.role == 'admin' or request.user.is_superuser:
        prescriptions = Prescription.objects.all()
    else:
        raise PermissionDenied
    
    # Search/filter by doctor name, patient name (admin), or notes
    if q:
        from django.db.models import Q
        prescriptions = prescriptions.filter(
            Q(doctor__user__first_name__icontains=q) |
            Q(doctor__user__last_name__icontains=q) |
            Q(patient__user__first_name__icontains=q) |
            Q(patient__user__last_name__icontains=q) |
            Q(additional_notes__icontains=q) |
            Q(items__medication_name__icontains=q)
        ).distinct()
    
    prescriptions = prescriptions.order_by('-created_at')
    
    return render(request, 'prescriptions/prescription_list.html', {
        'prescriptions': prescriptions,
        'search_query': q,
    })

@login_required
def download_prescription_pdf(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    # Auth check: patient must own it, or doctor/admin
    is_patient = (request.user.role == 'patient' and prescription.patient.user == request.user)
    is_doctor = (request.user.role == 'doctor' and prescription.doctor.user == request.user)
    is_admin = request.user.role == 'admin' or request.user.is_superuser
    
    if not (is_patient or is_doctor or is_admin):
        raise PermissionDenied("You are not authorized to view this prescription.")
        
    context = {
        'prescription': prescription,
        'items': prescription.items.all(),
        'doctor': prescription.doctor,
        'patient': prescription.patient
    }
    
    pdf = render_to_pdf('prescriptions/pdf_template.html', context)
    if pdf:
        response = HttpResponse(pdf.content, content_type='application/pdf')
        filename = f"Prescription_{prescription.patient.user.last_name}_{prescription.date_written.strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'filename="{filename}"'
        return response
    return HttpResponse("Error generating PDF", status=500)
