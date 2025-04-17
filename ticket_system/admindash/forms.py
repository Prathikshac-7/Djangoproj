from django import forms
from django.contrib.auth.models import User

# Role dropdown options
ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Agent', 'Agent'),
    ('Customer', 'Customer'),
]

class CustomSignupForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        
        return cleaned_data

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class CreateAgentForm(forms.Form):
    name = forms.CharField(max_length=100, label="Agent Name")
    email = forms.EmailField(label="Agent Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        
        return cleaned_data
