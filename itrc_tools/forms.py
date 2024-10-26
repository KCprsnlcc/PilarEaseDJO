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
        
from django.contrib.auth import get_user_model
from main.models import UserProfile
from .models import CustomUser 

CustomUser = get_user_model()
class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'student_id',
            'full_name',
            'academic_year_level',
            'contact_number',
            'is_counselor',
            'is_itrc_staff',
            'is_active',
            'password',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create or update UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.avatar = self.cleaned_data.get('avatar') or profile.avatar
            profile.save()
        return user

class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'student_id',
            'full_name',
            'academic_year_level',
            'contact_number',
            'is_counselor',
            'is_itrc_staff',
            'is_active',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            # Update UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            if self.cleaned_data.get('avatar'):
                profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        return user