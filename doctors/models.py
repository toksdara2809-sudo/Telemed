from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=200, help_text="e.g. MBBS, MD, PhD")
    bio = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profile_picture = models.ImageField(
        upload_to='doctors/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text="Profile photo (JPG, PNG, or GIF — max 5MB)."
    )
    is_available = models.BooleanField(default=True, help_text="Overall status: toggles if patient can see doctor as active/busy.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.specialization})"

class DoctorAvailability(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(max_length=15, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Doctor Availabilities"
        # Avoid duplicate schedule slots for same doctor/day/time
        unique_together = ('doctor', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week}: {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
