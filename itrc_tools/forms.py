# itrc_tools/forms.py
from .constants import ROLE_CHOICES
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
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Role')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    is_active = forms.BooleanField(required=False, label='Active', initial=True)  # Added is_active

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'student_id',
            'full_name',
            'academic_year_level',
            'contact_number',
            'is_active',  # Include is_active in fields
            'password',
            'role',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'email': forms.EmailInput(attrs={'class': 'itrc-add-user-input'}),
            'student_id': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'full_name': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'academic_year_level': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'itrc-add-user-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'pilarease-itrc-toggle-checkbox'}),
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
        role = self.cleaned_data['role']
        user.is_active = self.cleaned_data['is_active']  # Set is_active

        # Set role-based flags
        if role == 'student':
            user.is_counselor = False
            user.is_itrc_staff = False
        elif role == 'counselor':
            user.is_counselor = True
            user.is_itrc_staff = False
        elif role == 'itrc_staff':
            user.is_counselor = False
            user.is_itrc_staff = True

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
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Role')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep the current password'}),
        required=False,
        label='Password'
    )
    student_id = forms.CharField(
        required=False,
        label='Student ID',
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'itrc-edit-user-input-field'})
    )
    avatar = forms.ImageField(required=False, label='Avatar')  # Added avatar field
    is_active = forms.BooleanField(required=False, label='Active')  # Added is_active

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'student_id',
            'full_name',
            'academic_year_level',
            'contact_number',
            'is_active',  # Include is_active in fields
            'password',
            'role',
            'avatar',  # Include avatar in fields
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'itrc-edit-user-input-field'}),
            'email': forms.EmailInput(attrs={'class': 'itrc-edit-user-input-field'}),
            'full_name': forms.TextInput(attrs={'class': 'itrc-edit-user-input-field'}),
            'academic_year_level': forms.TextInput(attrs={'class': 'itrc-edit-user-input-field'}),
            'contact_number': forms.TextInput(attrs={'class': 'itrc-edit-user-input-field'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'pilarease-itrc-toggle-checkbox'}),
            'role': forms.Select(attrs={'class': 'itrc-edit-user-input-dropdown'}),
        }
        help_texts = {
            'password': 'Enter a new password if you want to change it.',
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        if self.instance:
            # Set initial role based on flags
            if self.instance.is_itrc_staff:
                self.fields['role'].initial = 'itrc_staff'
            elif self.instance.is_counselor:
                self.fields['role'].initial = 'counselor'
            else:
                self.fields['role'].initial = 'student'
            
            # Set initial is_active value
            self.fields['is_active'].initial = self.instance.is_active

            # Populate initial values for UserProfile fields
            try:
                profile = self.instance.profile
                self.fields['avatar'].initial = profile.avatar
                # If you have a 'bio' field, uncomment the next line
                # self.fields['bio'].initial = profile.bio
            except UserProfile.DoesNotExist:
                pass

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use by another user.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        role = self.cleaned_data['role']
        user.is_active = self.cleaned_data['is_active']  # Set is_active

        # Set role-based flags
        if role == 'student':
            user.is_counselor = False
            user.is_itrc_staff = False
        elif role == 'counselor':
            user.is_counselor = True
            user.is_itrc_staff = False
        elif role == 'itrc_staff':
            user.is_counselor = False
            user.is_itrc_staff = True

        if password:
            user.set_password(password)

        if commit:
            user.save()
            # Update UserProfile fields
            profile, created = UserProfile.objects.get_or_create(user=user)
            if self.cleaned_data.get('avatar'):
                profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        return user