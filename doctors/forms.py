from django import forms
from .models import DoctorProfile, DoctorAvailability
from django.contrib.auth import get_user_model

User = get_user_model()

class DoctorUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ('specialization', 'qualifications', 'bio', 'consultation_fee', 'profile_picture', 'is_available')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ('day_of_week', 'start_time', 'end_time')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
