from django import forms
from .models import PatientProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('date_of_birth', 'gender', 'contact_number', 'blood_group', 'allergies', 'emergency_contact_name', 'emergency_contact_phone', 'address')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
