from django import forms
from django.utils import timezone
from .models import (
    AppointmentSchedule, 
    Appointment, 
    BlockedTimeSlot, 
    AppointmentReport
)
from django.contrib.auth import get_user_model

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class AppointmentScheduleForm(forms.ModelForm):
    class Meta:
        model = AppointmentSchedule
        fields = ['counselor', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['counselor'].queryset = User.objects.filter(is_counselor=True)
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be later than start time.")
        
        return cleaned_data

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['counselor', 'title', 'description', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if 'counselor' in self.fields:
            self.fields['counselor'].queryset = User.objects.filter(is_counselor=True)
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        # Ensure date is not in the past
        if date and date < timezone.now().date():
            raise forms.ValidationError("Cannot schedule appointments in the past.")
        
        # Ensure end_time is after start_time
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be later than start time.")
        
        return cleaned_data

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

class BlockedTimeSlotForm(forms.ModelForm):
    class Meta:
        model = BlockedTimeSlot
        fields = ['counselor', 'date', 'start_time', 'end_time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['counselor'].queryset = User.objects.filter(is_counselor=True)
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        # Ensure date is not in the past
        if date and date < timezone.now().date():
            raise forms.ValidationError("Cannot block slots in the past.")
        
        # Ensure end_time is after start_time
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be later than start time.")
        
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
