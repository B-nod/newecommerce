from django import forms
from django.forms import ModelForm
# from products.models import Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    dob = forms.DateField(help_text="Enter your date of birth (YYYY-MM-DD)")
    contact = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'dob', 'contact', 'address', 'email', 'username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

