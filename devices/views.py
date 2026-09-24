from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from authentication.permissions import patient_required
from .models import BloodPressureReading, AIDiagnosisHistory
from .services.diagnosis import predict_condition, SYMPTOMS, get_drug_recommendations
from patients.models import PatientProfile
from appointments.models import Appointment
from notifications.models import Notification
from doctors.models import DoctorProfile
from prescriptions.models import Prescription, PrescriptionItem

@login_required
def view_readings(request):
    if request.user.role == 'patient':
        patient = get_object_or_404(PatientProfile, user=request.user)
    else:
        patient_id = request.GET.get('patient_id')
        if not patient_id:
            messages.error(request, "Patient ID is required.")
            return redirect('dashboard_home')
        patient = get_object_or_404(PatientProfile, id=patient_id)
        
    readings = BloodPressureReading.objects.filter(patient=patient).order_by('timestamp')
    
    # Format data for Chart.js trend lines
    chart_data = {
        'timestamps': [r.timestamp.strftime('%Y-%m-%d %H:%M') for r in readings],
        'systolic': [r.systolic for r in readings],
        'diastolic': [r.diastolic for r in readings],
        'pulse': [r.pulse for r in readings]
    }
    
    return render(request, 'devices/readings.html', {
        'patient': patient,
        'readings': readings.reverse(), # list recent first in table
        'chart_data': chart_data
    })

@login_required
@require_POST
def record_reading(request):
    """
    Ingest endpoint used by BOTH the Web Bluetooth UI and the Device Simulator.
    """
    if request.user.role != 'patient':
        return JsonResponse({'error': 'Only patients can record readings'}, status=403)
        
    patient = get_object_or_404(PatientProfile, user=request.user)
    
    try:
        systolic = int(request.POST.get('systolic'))
        diastolic = int(request.POST.get('diastolic'))
        pulse = int(request.POST.get('pulse'))
        device_id = request.POST.get('device_id', 'Simulator-BLE')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid numerical values for readings'}, status=400)

    reading = BloodPressureReading.objects.create(
        patient=patient,
        systolic=systolic,
        diastolic=diastolic,
        pulse=pulse,
        device_id=device_id
    )

    # Abnormal reading check (systolic > 140 or < 90, diastolic > 90 or < 60)
    is_abnormal = reading.is_abnormal
    if is_abnormal:
        # Find doctor of patient's latest appointment
        latest_app = Appointment.objects.filter(patient=patient).order_by('-date').first()
        if latest_app and latest_app.doctor:
            Notification.objects.create(
                recipient=latest_app.doctor.user,
                title="Abnormal Blood Pressure Alert!",
                message=f"Patient {patient.user.get_full_name()} has recorded an abnormal BP reading of {systolic}/{diastolic} mmHg with pulse {pulse} bpm."
            )

    return JsonResponse({
        'status': 'success',
        'reading': {
            'id': reading.id,
            'systolic': reading.systolic,
            'diastolic': reading.diastolic,
            'pulse': reading.pulse,
            'device_id': reading.device_id,
            'is_abnormal': is_abnormal,
            'timestamp': reading.timestamp.strftime('%Y-%m-%d %H:%M')
        }
    })

@login_required
@patient_required
def ble_simulator(request):
    """
    Virtual Bluetooth Simulator dashboard.
    """
    return render(request, 'devices/ble_simulator.html')

@login_required
def ai_diagnosis_flow(request):
    if request.user.role == 'patient':
        patient = get_object_or_404(PatientProfile, user=request.user)
    else:
        patient_id = request.GET.get('patient_id')
        if not patient_id:
            messages.error(request, "Patient ID is required.")
            return redirect('dashboard_home')
        patient = get_object_or_404(PatientProfile, id=patient_id)

    predictions = []
    selected_symptoms_list = []
    recommended_drugs = []
    top_condition = None
    
    if request.method == 'POST':
        # Check if this is a prescription save request
        if 'save_prescription' in request.POST and request.user.role == 'patient':
            top_condition = request.POST.get('top_condition', '')
            symptom_str = request.POST.get('symptom_str', '')
            selected_symptoms_list = request.POST.getlist('symptoms')
            
            recommended_drugs = get_drug_recommendations(top_condition)
            
            if recommended_drugs and top_condition:
                # Create a Prescription record (doctor=None — pending doctor assignment)
                try:
                    from consultations.models import Consultation
                    prescription = Prescription.objects.create(
                        patient=patient,
                        doctor=None,
                        additional_notes=f"AI-generated prescription based on symptom analysis.\n"
                                         f"Predicted condition: {top_condition}\n"
                                         f"Symptoms: {symptom_str}\n"
                                         f"Note: This is an AI suggestion and must be reviewed by a doctor."
                    )
                    for drug in recommended_drugs:
                        PrescriptionItem.objects.create(
                            prescription=prescription,
                            medication_name=drug['name'],
                            dosage=drug['dosage'],
                            frequency=drug['frequency'],
                            duration=drug['duration']
                        )
                    
                    messages.success(request, f"AI prescription saved! A doctor will review it shortly.")
                except Exception as e:
                    messages.error(request, f"Could not save prescription: {e}")
            return redirect('prescription_list')
        
        # Regular symptom analysis
        selected_symptoms_list = request.POST.getlist('symptoms')
        if selected_symptoms_list:
            predictions = predict_condition(selected_symptoms_list)
            
            # Persist highest prediction as diagnosis suggestion
            if request.user.role == 'patient' and predictions:
                top_condition, confidence = predictions[0]
                AIDiagnosisHistory.objects.create(
                    patient=patient,
                    symptoms=", ".join([s.replace('_', ' ').title() for s in selected_symptoms_list]),
                    predicted_condition=top_condition,
                    confidence=confidence
                )
                recommended_drugs = get_drug_recommendations(top_condition)
                messages.success(request, "AI Analysis completed. Results and drug suggestions below.")
        else:
            messages.error(request, "Please select at least one symptom for analysis.")
            
    # Format symptom list for UI checkboxes
    ui_symptoms = [{'key': s, 'name': s.replace('_', ' ').title()} for s in SYMPTOMS]
    
    # Get recent AI analysis history
    history = AIDiagnosisHistory.objects.filter(patient=patient).order_by('-timestamp')[:5]

    return render(request, 'devices/ai_diagnosis.html', {
        'patient': patient,
        'symptoms': ui_symptoms,
        'selected_symptoms': selected_symptoms_list,
        'predictions': predictions,
        'history': history,
        'recommended_drugs': recommended_drugs,
        'top_condition': top_condition,
    })
