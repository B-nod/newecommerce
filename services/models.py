from django.db import models
from django.core  import validators
from django.core.validators import *

class Submission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(validators=[MinLengthValidator(9), MaxLengthValidator(10)], max_length=100)
    address = models.CharField(max_length=100)
    service = models.TextField()

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name