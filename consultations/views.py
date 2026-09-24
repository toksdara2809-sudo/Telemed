import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from appointments.models import Appointment
from .models import Consultation, ChatMessage
from medical_records.models import MedicalRecord
from patients.models import PatientProfile
from doctors.models import DoctorProfile

@login_required
def consultation_room(request, appointment_id):
    # Retrieve appointment and ensure it's approved
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.status != 'approved' and appointment.status != 'completed':
        messages.error(request, "Consultation is only available for approved or completed appointments.")
        return redirect('dashboard_home')
        
    # Check permissions (must be the patient or the doctor)
    is_patient = (request.user.role == 'patient' and appointment.patient.user == request.user)
    is_doctor = (request.user.role == 'doctor' and appointment.doctor.user == request.user)
    is_admin = request.user.role == 'admin' or request.user.is_superuser
    
    if not (is_patient or is_doctor or is_admin):
        return HttpResponseForbidden("You are not authorized to access this consultation room.")

    # Get or create the consultation record
    consultation, created = Consultation.objects.get_or_create(appointment=appointment)
    
    return render(request, 'consultations/room.html', {
        'appointment': appointment,
        'consultation': consultation,
        'is_doctor': is_doctor,
        'is_patient': is_patient
    })

@login_required
def get_messages(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Auth check
    appointment = consultation.appointment
    is_patient = (request.user.role == 'patient' and appointment.patient.user == request.user)
    is_doctor = (request.user.role == 'doctor' and appointment.doctor.user == request.user)
    is_admin = request.user.role == 'admin' or request.user.is_superuser
    if not (is_patient or is_doctor or is_admin):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Fetch messages sent after the provided message ID
    last_msg_id = request.GET.get('last_msg_id', 0)
    messages_qs = ChatMessage.objects.filter(consultation=consultation, id__gt=last_msg_id).order_by('timestamp')

    messages_list = []
    for msg in messages_qs:
        messages_list.append({
            'id': msg.id,
            'sender': msg.sender.get_full_name() or msg.sender.username,
            'sender_name': msg.sender.get_full_name() or msg.sender.username,
            'sender_id': msg.sender.id,
            'content': msg.message,
            'timestamp': msg.timestamp.strftime('%I:%M %p')
        })

    return JsonResponse({'messages': messages_list})

@login_required
@require_POST
def send_message(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Auth check
    appointment = consultation.appointment
    is_patient = (request.user.role == 'patient' and appointment.patient.user == request.user)
    is_doctor = (request.user.role == 'doctor' and appointment.doctor.user == request.user)
    if not (is_patient or is_doctor):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Support both JSON and form-encoded POST
    if request.content_type == 'application/json':
        try:
            body = json.loads(request.body)
            message_text = (body.get('content') or body.get('message') or '').strip()
        except (json.JSONDecodeError, AttributeError):
            message_text = ''
    else:
        message_text = (request.POST.get('content') or request.POST.get('message') or '').strip()
    if message_text:
        msg = ChatMessage.objects.create(
            consultation=consultation,
            sender=request.user,
            message=message_text
        )
        return JsonResponse({
            'status': 'success',
            'message': {
                'id': msg.id,
                'sender': msg.sender.get_full_name() or msg.sender.username,
                'sender_name': msg.sender.get_full_name() or msg.sender.username,
                'sender_id': msg.sender.id,
                'content': msg.message,
                'timestamp': msg.timestamp.strftime('%I:%M %p')
            }
        })
        
    return JsonResponse({'error': 'Empty message'}, status=400)

@login_required
@require_POST
def complete_consultation(request, consultation_id):
    # Only doctors can complete and save notes
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Only doctors can complete consultations.")
        
    consultation = get_object_or_404(Consultation, id=consultation_id)
    appointment = consultation.appointment
    
    if appointment.doctor.user != request.user:
        return HttpResponseForbidden("You are not the designated doctor for this consultation.")

    diagnosis = request.POST.get('diagnosis', '').strip()
    treatment_plan = request.POST.get('treatment_plan', '').strip()
    notes = request.POST.get('doctor_notes', '').strip()
    
    if not diagnosis or not treatment_plan:
        messages.error(request, "Diagnosis and Treatment Plan are required to complete the consultation.")
        return redirect('consultation_room', appointment_id=appointment.id)

    # Update consultation status and notes
    consultation.status = 'completed'
    consultation.doctor_notes = notes
    consultation.save()
    
    # Update appointment status
    appointment.status = 'completed'
    appointment.save()
    
    # Create EMR MedicalRecord
    MedicalRecord.objects.create(
        patient=appointment.patient,
        doctor=appointment.doctor,
        diagnosis=diagnosis,
        treatment_plan=treatment_plan,
        notes=notes
    )
    
    messages.success(request, "Consultation completed and saved to patient's Medical Records (EMR).")
    return redirect('dashboard_doctor')
