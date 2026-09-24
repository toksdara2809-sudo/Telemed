from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from authentication.permissions import patient_required, doctor_required, admin_required
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from appointments.models import Appointment
from consultations.models import Consultation
from medical_records.models import MedicalRecord
from prescriptions.models import Prescription
from notifications.models import Notification
import datetime

User = get_user_model()

def landing_page(request):
    """Public landing page — shows the marketing site for unauthenticated users.
       Authenticated users are redirected straight to their dashboard."""
    if request.user.is_authenticated:
        if request.user.role == 'patient':
            return redirect('dashboard_patient')
        elif request.user.role == 'doctor':
            return redirect('dashboard_doctor')
        elif request.user.role == 'admin' or request.user.is_superuser:
            return redirect('dashboard_admin')
        return redirect('login')
    return render(request, 'landing.html')

@login_required
def dashboard_home(request):
    if request.user.role == 'patient':
        return redirect('dashboard_patient')
    elif request.user.role == 'doctor':
        return redirect('dashboard_doctor')
    elif request.user.role == 'admin' or request.user.is_superuser:
        return redirect('dashboard_admin')
    return redirect('login')

@login_required
@patient_required
def dashboard_patient(request):
    patient = get_object_or_404(PatientProfile, user=request.user)

    # Filterable appointment history
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        date__gte=datetime.date.today(),
        status__in=['pending', 'approved']
    ).order_by('date', 'time_slot')

    # All appointments (for history) — apply optional filters
    all_appointments = Appointment.objects.filter(patient=patient)
    if status_filter:
        all_appointments = all_appointments.filter(status=status_filter)
    if date_from:
        all_appointments = all_appointments.filter(date__gte=date_from)
    if date_to:
        all_appointments = all_appointments.filter(date__lte=date_to)
    all_appointments = all_appointments.order_by('-date', 'time_slot')

    consultations = Consultation.objects.filter(appointment__patient=patient).order_by('-created_at')[:5]
    records_summary = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')[:3]
    active_prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')[:3]
    
    return render(request, 'dashboard/patient_dashboard.html', {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'all_appointments': all_appointments,
        'consultations': consultations,
        'records_summary': records_summary,
        'active_prescriptions': active_prescriptions,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    })

@login_required
@doctor_required
def dashboard_doctor(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    today = datetime.date.today()
    
    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=today,
        status='approved'
    ).order_by('time_slot')
    
    pending_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='pending'
    ).order_by('date', 'time_slot')
    
    active_consultations = Consultation.objects.filter(
        appointment__doctor=doctor,
        status='active'
    ).order_by('-created_at')

    return render(request, 'dashboard/doctor_dashboard.html', {
        'doctor': doctor,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'active_consultations': active_consultations,
    })

@login_required
@admin_required
def dashboard_admin(request):
    total_patients = PatientProfile.objects.count()
    total_doctors = DoctorProfile.objects.count()
    total_appointments = Appointment.objects.count()
    
    # List pending doctor approvals
    pending_doctors = User.objects.filter(role='doctor', is_approved_doctor=False)
    
    # List recently registered patients and doctors
    recent_patients = PatientProfile.objects.order_by('-created_at')[:5]
    recent_doctors = DoctorProfile.objects.order_by('-created_at')[:5]
    
    return render(request, 'dashboard/admin_dashboard.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'pending_doctors': pending_doctors,
        'recent_patients': recent_patients,
        'recent_doctors': recent_doctors,
    })

@login_required
@admin_required
def approve_doctor(request, doctor_user_id):
    doctor_user = get_object_or_404(User, id=doctor_user_id, role='doctor')
    doctor_user.is_approved_doctor = True
    doctor_user.save()
    
    # Also ensure a DoctorProfile is instantiated if it wasn't already
    DoctorProfile.objects.get_or_create(
        user=doctor_user,
        defaults={'specialization': 'General Practitioner', 'qualifications': 'MBBS', 'bio': 'Awaiting bio setup'}
    )
    
    messages.success(request, f"Doctor account {doctor_user.username} has been approved.")
    
    # Notify doctor
    Notification.objects.create(
        recipient=doctor_user,
        title="Account Approved",
        message="Your doctor account has been approved by the administrator. You can now configure availability and take consultations."
    )
    
    return redirect('dashboard_admin')

@login_required
def global_search(request):
    query = request.GET.get('q', '').strip()
    role = request.user.role
    results_doctors = []
    results_patients = []
    results_appointments = []
    
    if query:
        if role == 'patient':
            # Patients search doctors by name or specialization
            results_doctors = DoctorProfile.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(specialization__icontains=query),
                user__is_approved_doctor=True
            )
        elif role == 'doctor':
            # Doctors search patients or their appointments
            doctor = get_object_or_404(DoctorProfile, user=request.user)
            results_patients = PatientProfile.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(blood_group__icontains=query) |
                Q(allergies__icontains=query)
            )
            results_appointments = Appointment.objects.filter(
                Q(patient__user__first_name__icontains=query) |
                Q(patient__user__last_name__icontains=query) |
                Q(reason__icontains=query),
                doctor=doctor
            )
        elif role == 'admin' or request.user.is_superuser:
            # Admins search patients, doctors, and appointments
            results_patients = PatientProfile.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )
            results_doctors = DoctorProfile.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(specialization__icontains=query)
            )
            results_appointments = Appointment.objects.filter(
                Q(patient__user__first_name__icontains=query) |
                Q(patient__user__last_name__icontains=query) |
                Q(doctor__user__first_name__icontains=query) |
                Q(doctor__user__last_name__icontains=query)
            )

    # Paginate results
    # Simple pagination helper
    def paginate_queryset(qs, page_number):
        paginator = Paginator(qs, 10)
        return paginator.get_page(page_number)
        
    page = request.GET.get('page', 1)
    
    return render(request, 'dashboard/search_results.html', {
        'query': query,
        'doctors': paginate_queryset(results_doctors, page) if results_doctors else [],
        'patients': paginate_queryset(results_patients, page) if results_patients else [],
        'appointments': paginate_queryset(results_appointments, page) if results_appointments else [],
    })
