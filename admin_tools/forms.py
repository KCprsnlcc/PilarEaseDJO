# admin_tools/forms.py

from django import forms
from import_export.forms import ImportForm
from main.models import Dataset

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['csv_file']
        widgets = {
            'csv_file': forms.ClearableFileInput(attrs={'accept': '.csv'}),
        }
