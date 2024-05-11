from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.testFunc),
    path('', views.product_show, name='allproducts'),
    path('addproduct/',views.post_product, name='addproduct'),
    path('addcategory/',views.post_category, name='addcategory'),
    path('category/', views.category_show, name='allcategories'),
    path('updateproduct/<int:product_id>', views.update_product, name='updateproduct'),
    path('deleteproduct/<int:product_id>', views.delete_product, name='deleteproduct'),
    path('updatecategory/<int:category_id>', views.update_category, name='updatecategory'),
    path('deletecategory/<int:category_id>', views.delete_category, name='deletecategory'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='addtocart'),
    path('mycart/', views.show_cart_item, name='mycart'),
    path('deletecartitems/<int:cart_id>', views.remove_cart_item, name='removecart'),
    path('orderitemform/<int:product_id>/<int:cart_id>', views.order_item, name='orders'),
    path('my_order', views.my_order, name='myorder'),
    path('allorder', views.all_order, name='allorders'),
    path('esewaform/',views.EsewaView.as_view(), name='esewaform'),
    path('esewaverify/<int:order_id>/<int:cart_id>', views.esewa_verify, name='esewaverify'),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    
]
