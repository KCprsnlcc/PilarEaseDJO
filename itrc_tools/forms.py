# itrc_tools/forms.py

from django import forms
from .models import SystemSetting

class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ['auto_accept_enabled', 'auto_reject_enabled']
        widgets = {
            'auto_accept_enabled': forms.CheckboxInput(attrs={'class': 'pilarease-itrc-form-checkbox'}),
            'auto_reject_enabled': forms.CheckboxInput(attrs={'class': 'pilarease-itrc-form-checkbox'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        auto_accept = cleaned_data.get('auto_accept_enabled')
        auto_reject = cleaned_data.get('auto_reject_enabled')

        if auto_accept and auto_reject:
            raise forms.ValidationError("You cannot enable both Auto Accept and Auto Reject at the same time.")

        return cleaned_data
        
from django.contrib.auth import get_user_model
from main.models import UserProfile
from .models import CustomUser 

CustomUser = get_user_model()

class AddUserForm(forms.ModelForm):
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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'email': forms.EmailInput(attrs={'class': 'itrc-add-user-input'}),
            'student_id': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'full_name': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'academic_year_level': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'is_counselor': forms.CheckboxInput(attrs={'class': 'itrc-add-user-input-checkbox'}),
            'is_itrc_staff': forms.CheckboxInput(attrs={'class': 'itrc-add-user-input-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'itrc-add-user-input-checkbox'}),
            'password': forms.PasswordInput(attrs={'class': 'itrc-add-user-input'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id').strip()
        if CustomUser.objects.filter(student_id__iexact=student_id).exists():
            raise forms.ValidationError("A user with this student ID already exists.")
        return student_id

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set the password properly
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'itrc-add-user-input-file'}),
        }
class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    avatar = forms.ImageField(required=False)
    verification_status = forms.ChoiceField(
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected')
        ],
        widget=forms.Select(attrs={'class': 'pilarease-itrc-form-select'})
    )

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
            'verification_status',  # Include verification_status
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