# itrc_tools/forms.py

from django import forms
from .models import SystemSetting

class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ['key', 'value']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'pilarease-itrc-form-input'}),
            'value': forms.TextInput(attrs={'class': 'pilarease-itrc-form-input'}),
        }
