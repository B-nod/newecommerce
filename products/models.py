from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from django.core  import validators

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    stock = models.IntegerField()
    image = models.FileField(upload_to='static/uploads', null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_data = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    PAYMENT=(
        ('Cash on delivery','Cash on delivery'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(default='Pending', max_length=200)
    payment_method = models.CharField(max_length=200, choices=PAYMENT)
    contact_no = models.IntegerField(validators=[MinLengthValidator(9), MaxLengthValidator(10)])
    address = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)