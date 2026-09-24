from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.contrib.auth.decorators import login_required
from authentication.permissions import admin_required
from appointments.models import Appointment
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from consultations.models import Consultation
import csv

@login_required
@admin_required
def reports_home(request):
    total_patients = PatientProfile.objects.count()
    total_doctors = DoctorProfile.objects.count()
    total_appointments = Appointment.objects.count()
    total_consultations = Consultation.objects.count()
    
    status_counts = Appointment.objects.values('status').annotate(count=Count('status'))
    
    return render(request, 'reports/reports_dashboard.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'total_consultations': total_consultations,
        'status_counts': status_counts,
    })

@login_required
@admin_required
def reports_json_data(request):
    # 1. Appointments by Month (for line chart)
    # Extract month name/number
    monthly_appointments = Appointment.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_labels = []
    monthly_counts = []
    for item in monthly_appointments:
        if item['month'] and 1 <= item['month'] <= 12:
            monthly_labels.append(months[item['month'] - 1])
            monthly_counts.append(item['count'])

    # 2. Consultations by Doctor (for bar chart)
    doctor_consultations = Appointment.objects.filter(status='completed').values(
        'doctor__user__last_name'
    ).annotate(count=Count('id')).order_by('-count')[:5]
    
    doc_labels = [f"Dr. {item['doctor__user__last_name']}" for item in doctor_consultations]
    doc_counts = [item['count'] for item in doctor_consultations]

    # 3. Appointment Status distribution (for pie chart)
    status_distribution = Appointment.objects.values('status').annotate(count=Count('id'))
    status_labels = [item['status'].capitalize() for item in status_distribution]
    status_counts = [item['count'] for item in status_distribution]

    return JsonResponse({
        'monthly_labels': monthly_labels or ["No Data"],
        'monthly_counts': monthly_counts or [0],
        'top_doctors': [{'name': name, 'count': ct} for name, ct in zip(doc_labels, doc_counts)] or [{'name': 'No Data', 'count': 0}],
        'status_labels': status_labels or ["No Data"],
        'status_counts': status_counts or [0],
    })

@login_required
@admin_required
def export_appointments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Appointment ID', 'Patient Name', 'Doctor Name', 'Date', 'Time Slot', 'Status', 'Reason'])
    
    appointments = Appointment.objects.all().select_related('patient__user', 'doctor__user').order_by('-date')
    for app in appointments:
        writer.writerow([
            app.id,
            app.patient.user.get_full_name(),
            f"Dr. {app.doctor.user.get_full_name()}",
            app.date.strftime('%Y-%m-%d'),
            app.time_slot.strftime('%I:%M %p'),
            app.status,
            app.reason
        ])
        
    return response
