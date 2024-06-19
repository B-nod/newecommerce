from django.urls import path
from . import views

urlpatterns = [
    path('form/',views.index, name='serviceform'),
    path('show/',views.services, name='serviceshow'),
]
