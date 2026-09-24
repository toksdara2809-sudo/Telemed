from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from patients.models import PatientProfile
from doctors.models import DoctorProfile

class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='created_records')
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    notes = models.TextField(blank=True, help_text="Doctor's notes or consultation summary.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"EMR for {self.patient.user.get_full_name()} - {self.created_at.strftime('%Y-%m-%d')}"

class LabResult(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='lab_results')
    uploading_doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='uploaded_labs')
    test_name = models.CharField(max_length=150)
    test_date = models.DateField()
    file = models.FileField(
        upload_to='lab_results/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx'])],
        help_text="Upload lab result file (PDF, image, or document — max 10MB)."
    )
    doctor_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} for {self.patient.user.get_full_name()}"
