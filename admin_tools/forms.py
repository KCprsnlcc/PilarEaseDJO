# admin_tools/forms.py

from django import forms
from main.models import Dataset
import pandas as pd

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['csv_file']  # Exclude 'name' field here
        widgets = {
            'csv_file': forms.ClearableFileInput(attrs={'accept': '.csv'}),
        }

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            # Validate file size (e.g., max 15MB)
            if csv_file.size > 15 * 1024 * 1024:
                raise forms.ValidationError("CSV file size must be under 15MB.")
            
            # Validate file extension
            if not csv_file.name.endswith('.csv'):
                raise forms.ValidationError("Only CSV files are allowed.")
            
            # Read and validate CSV content
            try:
                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(csv_file)
            except pd.errors.EmptyDataError:
                raise forms.ValidationError("Uploaded CSV file is empty.")
            except pd.errors.ParserError:
                raise forms.ValidationError("Error parsing CSV file. Please ensure it's a valid CSV.")
            
            # Define expected columns
            expected_columns = ['Text', 'Label']
            
            # Check if all expected columns are present (case-insensitive)
            df_columns = [col.strip().lower() for col in df.columns]
            expected_columns_lower = [col.lower() for col in expected_columns]
            
            missing_columns = [col for col in expected_columns_lower if col not in df_columns]
            if missing_columns:
                formatted_missing = [col.capitalize() for col in missing_columns]
                raise forms.ValidationError(
                    f"CSV must contain the following columns: {', '.join(formatted_missing)}."
                )
            
            # Optionally, check for additional unwanted columns
            allowed_columns = set(expected_columns_lower)
            extra_columns = [col for col in df_columns if col not in allowed_columns]
            if extra_columns:
                formatted_extra = [col.capitalize() for col in extra_columns]
                raise forms.ValidationError(
                    f"CSV contains unexpected columns: {', '.join(formatted_extra)}. Only 'Text' and 'Label' are allowed."
                )
            
            # Reset the file pointer so that the view can read it again
            csv_file.seek(0)
        
        return csv_file