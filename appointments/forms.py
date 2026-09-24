from django import forms
from .models import Appointment
from doctors.models import DoctorProfile

class AppointmentBookForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'time_slot', 'reason')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe your symptoms...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only list available doctors
        self.fields['doctor'].queryset = DoctorProfile.objects.filter(is_available=True, user__is_approved_doctor=True)
        self.fields['doctor'].widget.attrs.update({'class': 'form-select'})
