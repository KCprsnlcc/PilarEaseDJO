# itrc_tools/forms.py

from django import forms
from .models import SystemSetting
from django.core.validators import FileExtensionValidator
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
    # Include UserProfile fields
    avatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.ClearableFileInput(attrs={'class': 'itrc-edit-user-input-field'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'itrc-edit-user-input-field', 'rows': 4}),
        label='Bio'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'full_name',
            'academic_year_level',
            'contact_number',
            'is_counselor',
            'is_itrc_staff',
            'is_active',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep the current password'}),
        }
        help_texts = {
            'password': 'Enter a new password if you want to change it.',
        }

    def __init__(self, *args, **kwargs):
        # Pop the user instance if provided
        self.user = kwargs.pop('instance', None)
        super(EditUserForm, self).__init__(*args, instance=self.user, **kwargs)
        
        # Make student_id read-only
        if self.user:
            self.fields['student_id'] = forms.CharField(
                initial=self.user.student_id,
                required=False,
                label='Student ID',
                disabled=True,
                widget=forms.TextInput(attrs={'class': 'itrc-edit-user-input-field'})
            )
        
        # Populate initial values for UserProfile fields
            try:
                profile = self.user.profile
                self.fields['avatar'].initial = profile.avatar
                self.fields['bio'].initial = profile.bio
            except UserProfile.DoesNotExist:
                pass

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This email is already in use by another user.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            # You can add more password validations here if needed
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            # Update UserProfile fields
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.bio = self.cleaned_data.get('bio')
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                profile.avatar = avatar
            profile.save()
        return user