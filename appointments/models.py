from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from patients.models import PatientProfile
from doctors.models import DoctorProfile, DoctorAvailability
import datetime

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, help_text="Briefly describe symptoms or reason for booking.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        
        # 1. Date cannot be in the past
        if self.date < datetime.date.today():
            raise ValidationError("Appointment date cannot be in the past.")

        # 2. Check if the doctor has availability for this weekday and time
        # Get weekday name from the appointment date
        weekday_name = self.date.strftime('%A') # e.g. 'Monday'
        
        # Find if doctor has active availability covering this weekday
        availabilities = DoctorAvailability.objects.filter(
            doctor=self.doctor,
            day_of_week=weekday_name,
            is_active=True
        )
        
        valid_time = False
        for avail in availabilities:
            if avail.start_time <= self.time_slot <= avail.end_time:
                valid_time = True
                break
                
        if not valid_time:
            raise ValidationError(f"The doctor is not available on {weekday_name} at this time slot.")

        # 3. Check for double booking (no other pending or approved appointment at the same date and time for this doctor)
        conflicting_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            date=self.date,
            time_slot=self.time_slot,
            status__in=['pending', 'approved']
        )
        
        if self.pk:
            conflicting_appointments = conflicting_appointments.exclude(pk=self.pk)
            
        if conflicting_appointments.exists():
            raise ValidationError("This time slot is already booked for this doctor.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date} at {self.time_slot.strftime('%I:%M %p')}"
