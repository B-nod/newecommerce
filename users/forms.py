from django import forms
from django.forms import ModelForm
from products.models import Customer

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'