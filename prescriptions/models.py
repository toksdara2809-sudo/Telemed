from django.db import models
from django.conf import settings
from patients.models import PatientProfile
from doctors.models import DoctorProfile

class Prescription(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    date_written = models.DateField(auto_now_add=True)
    additional_notes = models.TextField(blank=True, help_text="General advice, dietary restrictions, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        doctor_name = f"Dr. {self.doctor.user.last_name}" if self.doctor else "Pending Doctor"
        return f"Prescription for {self.patient.user.get_full_name()} by {doctor_name} ({self.date_written})"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medication_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=50, help_text="e.g. 500mg, 1 tablet")
    frequency = models.CharField(max_length=100, help_text="e.g. Twice a day after meals")
    duration = models.CharField(max_length=50, help_text="e.g. 7 days, 1 month")

    def __str__(self):
        return f"{self.medication_name} - {self.dosage} ({self.frequency} for {self.duration})"
