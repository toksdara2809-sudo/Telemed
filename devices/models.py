from django.db import models
from django.conf import settings
from patients.models import PatientProfile

class BloodPressureReading(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='bp_readings')
    systolic = models.IntegerField(help_text="Systolic reading (e.g. 120)")
    diastolic = models.IntegerField(help_text="Diastolic reading (e.g. 80)")
    pulse = models.IntegerField(help_text="Heart rate / Pulse rate in bpm")
    device_id = models.CharField(max_length=100, default="Simulator-BLE")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - BP: {self.systolic}/{self.diastolic} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_abnormal(self):
        return self.systolic > 140 or self.systolic < 90 or self.diastolic > 90 or self.diastolic < 60

class AIDiagnosisHistory(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='ai_diagnoses')
    symptoms = models.TextField(help_text="Comma-separated symptoms selected by patient.")
    predicted_condition = models.CharField(max_length=200)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage confidence score (e.g. 85.50)")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "AI Diagnosis Histories"
        ordering = ['-timestamp']

    def __str__(self):
        return f"AI Prediction for {self.patient.user.get_full_name()}: {self.predicted_condition} ({self.confidence}%)"
