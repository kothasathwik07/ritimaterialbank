from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name','email', 'category', 'quantity','description', 'donator_name', 'current_with', 'image']

from .models import DonationRequest

class DonationRequestForm(forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = ['name','email', 'category', 'quantity', 'description', 'image', 'donator_name', 'contact_info']
