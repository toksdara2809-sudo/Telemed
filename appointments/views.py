from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.permissions import patient_required, doctor_required
from .models import Appointment
from .forms import AppointmentBookForm
from patients.models import PatientProfile
from doctors.models import DoctorProfile

@login_required
@patient_required
def book_appointment(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    
    if request.method == 'POST':
        form = AppointmentBookForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = 'pending'
            try:
                appointment.save()
                messages.success(request, "Your appointment has been booked and is pending doctor approval.")
                return redirect('dashboard_patient')
            except Exception as e:
                # Catch ValidationErrors from model full_clean()
                messages.error(request, f"Booking conflict: {e}")
        else:
            messages.error(request, "Failed to book appointment. Please verify the date and time.")
    else:
        # Pre-select doctor if passed as GET param
        doctor_id = request.GET.get('doctor')
        initial_data = {}
        if doctor_id:
            initial_data['doctor'] = get_object_or_404(DoctorProfile, id=doctor_id)
        form = AppointmentBookForm(initial=initial_data)
        
    return render(request, 'appointments/book_appointment.html', {'form': form})

@login_required
@patient_required
def cancel_appointment(request, appointment_id):
    patient = get_object_or_404(PatientProfile, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    
    if appointment.status in ['pending', 'approved']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment successfully cancelled.")
    else:
        messages.error(request, "Only pending or approved appointments can be cancelled.")
        
    return redirect('dashboard_patient')

@login_required
@doctor_required
def update_appointment_status(request, appointment_id):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    action = request.POST.get('action')
    
    if action == 'approve':
        appointment.status = 'approved'
        messages.success(request, "Appointment approved successfully.")
    elif action == 'reject':
        appointment.status = 'rejected'
        messages.success(request, "Appointment rejected.")
    elif action == 'complete':
        appointment.status = 'completed'
        messages.success(request, "Appointment marked as completed.")
    else:
        messages.error(request, "Invalid action requested.")
        
    appointment.save()
    return redirect('dashboard_doctor')
