from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.homepage, name='home'),
    path('allproducts/', views.productspage, name='productspage'),
    path('productdetails/<int:product_id>', views.product_detail, name='productdetail'),
    path('userprofile/',views.user_profile, name='userprofile'),
    path('recommendproduct/',views.recommend_product, name='recommendproduct'),

    #For password reset
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html"),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),name='password_reset_complete'),
]