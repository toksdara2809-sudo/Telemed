from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator'),
    )
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='patient')
    is_approved_doctor = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_patient(self):
        return self.role == 'patient'
        
    @property
    def is_doctor(self):
        return self.role == 'doctor'
        
    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser
