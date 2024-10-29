from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Status, Feedback
from django import forms
from itrc_tools.models import EnrollmentMasterlist
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [
            'student_id', 'username', 'full_name', 'academic_year_level',
            'contact_number', 'email', 'password1', 'password2'
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        full_name = cleaned_data.get('full_name')
        academic_year_level = cleaned_data.get('academic_year_level')
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The passwords you entered do not match. Please try again.")

        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "This email address is already registered. Please log in or use a different email.")

        # Validate that the provided student_id, full_name, and academic_year_level match a record in EnrollmentMasterlist
        if student_id and full_name and academic_year_level:
            try:
                EnrollmentMasterlist.objects.get(
                    student_id=student_id.strip(),
                    full_name=full_name.strip(),
                    academic_year_level=academic_year_level.strip()
                )
            except EnrollmentMasterlist.DoesNotExist:
                self.add_error(None, "Your details do not match our enrollment records. Please check and try again.")
        else:
            self.add_error(None, "Please fill in all required fields.")

        return cleaned_data
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'}))

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')
        
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['emotion', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'editable-div', 'contenteditable': 'true'}),
        }

class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField()
    
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
