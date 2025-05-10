from django import forms
from hms.models import Doctor

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'department', 'contact_number', 'email']
