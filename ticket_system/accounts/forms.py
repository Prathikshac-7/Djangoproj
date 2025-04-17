from django import forms

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


class CustomLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
