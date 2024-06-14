import django_filters
from products.models import *
from django_filters import CharFilter, ModelChoiceFilter

class ProductFilter(django_filters.FilterSet):
    product_name_contains = CharFilter(field_name='product_name', lookup_expr='icontains')
    # category = ModelChoiceFilter(field_name='category', queryset=Category.objects.all(), label='Category')
    class Meta:
        model = Product
        fields = ['category']
        exclude = ['product_price', 'stock', 'image', 'description','created_at']
