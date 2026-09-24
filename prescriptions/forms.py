from django import forms
from django.forms import inlineformset_factory
from .models import Prescription, PrescriptionItem

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('patient', 'consultation', 'additional_notes')
        widgets = {
            'additional_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs.update({'class': 'form-select'})
        if 'consultation' in self.fields:
            self.fields['consultation'].widget.attrs.update({'class': 'form-select'})

PrescriptionItemFormSet = inlineformset_factory(
    Prescription,
    PrescriptionItem,
    fields=('medication_name', 'dosage', 'frequency', 'duration'),
    extra=3,
    can_delete=True,
    widgets={
        'medication_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Paracetamol'}),
        'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500mg'}),
        'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3 times daily'}),
        'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5 days'}),
    }
)
