# admin_tools/resources.py

from import_export import resources
from main.models import Dataset

class DatasetResource(resources.ModelResource):
    class Meta:
        model = Dataset
        fields = ('id', 'user', 'csv_file', 'uploaded_at')
        export_order = ('id', 'user', 'csv_file', 'uploaded_at')
