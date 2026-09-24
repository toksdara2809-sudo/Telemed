from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from authentication.permissions import doctor_required, patient_required
from .models import MedicalRecord, LabResult
from .forms import MedicalRecordForm, LabResultForm
from patients.models import PatientProfile
from doctors.models import DoctorProfile

@login_required
def view_my_records(request):
    # Patient sees their own record, doctor can see patient records by passing patient_id
    if request.user.role == 'patient':
        patient = get_object_or_404(PatientProfile, user=request.user)
    elif request.user.role in ['doctor', 'admin'] or request.user.is_superuser:
        patient_id = request.GET.get('patient_id')
        if not patient_id:
            messages.error(request, "Patient ID is required.")
            return redirect('dashboard_home')
        patient = get_object_or_404(PatientProfile, id=patient_id)
    else:
        raise PermissionDenied

    records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
    labs = LabResult.objects.filter(patient=patient).order_by('-test_date')
    
    return render(request, 'medical_records/patient_records.html', {
        'patient': patient,
        'records': records,
        'labs': labs
    })

@login_required
@doctor_required
def add_medical_record(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient_id = request.GET.get('patient_id')
    initial_data = {}
    if patient_id:
        initial_data['patient'] = get_object_or_404(PatientProfile, id=patient_id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.doctor = doctor
            record.save()
            messages.success(request, "Medical record added successfully.")
            return redirect(f"/records/view/?patient_id={record.patient.id}")
        else:
            messages.error(request, "Error adding medical record. Please verify inputs.")
    else:
        form = MedicalRecordForm(initial=initial_data)
        
    return render(request, 'medical_records/add_record.html', {'form': form})

@login_required
@doctor_required
def upload_lab_result(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient_id = request.GET.get('patient_id')
    initial_data = {}
    if patient_id:
        initial_data['patient'] = get_object_or_404(PatientProfile, id=patient_id)

    if request.method == 'POST':
        form = LabResultForm(request.POST, request.FILES)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.uploading_doctor = doctor
            lab.save()
            messages.success(request, "Lab result report uploaded successfully.")
            return redirect(f"/records/view/?patient_id={lab.patient.id}")
        else:
            messages.error(request, "Error uploading lab result. Make sure a file is selected.")
    else:
        form = LabResultForm(initial=initial_data)
        
    return render(request, 'medical_records/upload_lab.html', {'form': form})
