from django import forms
from .models import Permitir, Bloquear, DNSQuery

class PermitirForm(forms.ModelForm):
    class Meta:
        model = Permitir
        fields = ['port', 'domain', 'action']

class BloquearForm(forms.ModelForm):
    class Meta:
        model = Bloquear
        fields = ['port', 'domain', 'action']

class DNSQueryForm(forms.ModelForm):
    class Meta:
        model = DNSQuery
        fields = ['domain']
        widgets = {
            'domain': forms.TextInput(attrs={'placeholder': 'Enter domain...'}),
        }
