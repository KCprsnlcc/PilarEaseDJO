# itrc_tools/resources.py

from import_export import resources, fields
from .models import EnrollmentMasterlist

class EnrollmentMasterlistResource(resources.ModelResource):
    student_id = fields.Field(attribute='student_id', column_name='student_id')
    full_name = fields.Field(attribute='full_name', column_name='full_name')
    academic_year_level = fields.Field(attribute='academic_year_level', column_name='academic_year_level')
    # Removed contact_number and email fields

    class Meta:
        model = EnrollmentMasterlist
        import_id_fields = ('student_id',)
        fields = ('student_id', 'full_name', 'academic_year_level')
