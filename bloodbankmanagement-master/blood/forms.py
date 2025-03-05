from django import forms
from . import models
from .models import BloodRequest
from .models import DonationSchedule

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['bloodgroup', 'unit', 'reason','urgency_level','is_emergency','last_date']
        widgets = {
            'bloodgroup': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'urgency_level': forms.Select(attrs={'class': 'form-control'}),
            'is_emergency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'last_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Date input field


        }


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['patient_name','reason','bloodgroup','unit']

class DonationScheduleForm(forms.ModelForm):
    class Meta:
        model = DonationSchedule
        fields = ['hospital', 'donation_date']
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }