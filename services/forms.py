from django import forms
from .models import *

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
