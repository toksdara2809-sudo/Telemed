from django.db import models
from django.conf import settings
from appointments.models import Appointment

class Consultation(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    doctor_notes = models.TextField(blank=True, help_text="Notes to be transferred to Patient's EMR.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation for Appointment #{self.appointment.id}"

class ChatMessage(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}..."
