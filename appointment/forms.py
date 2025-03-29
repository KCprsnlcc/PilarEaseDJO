from django import forms
from django.utils import timezone
from .models import (
    AppointmentSchedule, 
    Appointment, 
    AppointmentFeedback, 
    BlockedTimeSlot, 
    AppointmentReport
)

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class AppointmentScheduleForm(forms.ModelForm):
    class Meta:
        model = AppointmentSchedule
        fields = ['counselor', 'date', 'start_time', 'end_time', 'is_available']
        widgets = {
            'date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')
        
        if date and date < timezone.now().date():
            raise forms.ValidationError("Cannot create schedule in the past")
            
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Start time must be before end time")
            
        return cleaned_data

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'user', 'counselor', 'schedule', 'title', 
            'description', 'date', 'start_time', 'end_time', 
            'status', 'counselor_notes'
        ]
        widgets = {
            'date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
            'counselor_notes': forms.Textarea(attrs={'rows': 4}),
        }
        
class UpdateAppointmentStatusForm(forms.ModelForm):
    send_notification = forms.BooleanField(
        required=False, 
        initial=True,
        label="Send notification to user"
    )
    
    class Meta:
        model = Appointment
        fields = ['status', 'counselor_notes']
        widgets = {
            'counselor_notes': forms.Textarea(attrs={'rows': 3}),
        }

class AppointmentFeedbackForm(forms.ModelForm):
    class Meta:
        model = AppointmentFeedback
        fields = ['rating', 'comments', 'suggestions']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            'suggestions': forms.Textarea(attrs={'rows': 3}),
        }

class BlockedTimeSlotForm(forms.ModelForm):
    class Meta:
        model = BlockedTimeSlot
        fields = ['counselor', 'date', 'start_time', 'end_time', 'reason']
        widgets = {
            'date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Start time must be before end time")
            
        return cleaned_data

class AppointmentReportForm(forms.ModelForm):
    class Meta:
        model = AppointmentReport
        fields = ['title', 'report_type', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date must be before end date")
            
        return cleaned_data

class DateRangeFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=DateInput(),
        required=False
    )
    end_date = forms.DateField(
        widget=DateInput(),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date must be before end date")
            
        return cleaned_data
