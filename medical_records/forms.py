from django import forms
from .models import MedicalRecord, LabResult
from patients.models import PatientProfile

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('patient', 'diagnosis', 'treatment_plan', 'notes')
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'treatment_plan': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs.update({'class': 'form-select'})

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ('patient', 'test_name', 'test_date', 'file', 'doctor_comment')
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'test_name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'doctor_comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs.update({'class': 'form-select'})
