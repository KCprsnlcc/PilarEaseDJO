# itrc_tools/forms.py

from django import forms

class UploadMasterlistForm(forms.Form):
    csv_file = forms.FileField(label='Select CSV File', required=True, help_text='Upload a CSV file with headers: student_id, full_name, academic_year_level, contact_number, email')

from .models import SystemSetting

class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ['key', 'value']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'pilarease-admin-feedback-search-input'}),
            'value': forms.TextInput(attrs={'class': 'pilarease-admin-feedback-search-input'}),
        }
