from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from patients.models import PatientProfile
from doctors.models import DoctorProfile

User = get_user_model()

class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    # Profile fields
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    gender = forms.ChoiceField(choices=PatientProfile.GENDER_CHOICES, required=True)
    contact_number = forms.CharField(max_length=20, required=True)
    blood_group = forms.ChoiceField(choices=PatientProfile.BLOOD_GROUPS, required=True)
    allergies = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    emergency_contact_name = forms.CharField(max_length=100, required=True)
    emergency_contact_phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                contact_number=self.cleaned_data.get('contact_number'),
                blood_group=self.cleaned_data.get('blood_group'),
                allergies=self.cleaned_data.get('allergies'),
                emergency_contact_name=self.cleaned_data.get('emergency_contact_name'),
                emergency_contact_phone=self.cleaned_data.get('emergency_contact_phone'),
                address=self.cleaned_data.get('address')
            )
        return user

class DoctorCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    # Profile fields
    specialization = forms.CharField(max_length=100, required=True)
    qualifications = forms.CharField(max_length=200, required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'doctor'
        user.is_approved_doctor = True  # Created directly by admin
        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user,
                specialization=self.cleaned_data.get('specialization'),
                qualifications=self.cleaned_data.get('qualifications'),
                bio=self.cleaned_data.get('bio'),
                consultation_fee=self.cleaned_data.get('consultation_fee'),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user
