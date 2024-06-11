from django.db import models

# Create your models here.

class Blog(models.Model):
    title=models.CharField(max_length=200)
    image=models.FileField(upload_to='static/uploads', null=True)
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
