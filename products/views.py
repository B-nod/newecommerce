from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from . forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.auth import admin_only


# Create your views here.
def testFunc(request):
    return HttpResponse("this is test product")

@login_required
@admin_only
def product_show(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/index.html', context)

@login_required
@admin_only
def category_show(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'products/allcategory.html', context)

@login_required
@admin_only
def post_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "add product successfully !")
            return redirect('/products/addproduct')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify product field.')
            return render(request,'products/addproduct.html',{
                'form':form
            })
    
    context = {
        'form':ProductForm
    }

    return render(request, 'products/addproduct.html', context)

@login_required
@admin_only
def post_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "add category successfully !")
            return redirect('/products/addcategory')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify category field.')
            return render(request,'products/addcategory.html',{
                'form':form
            })
    
    context = {
        'form':CategoryForm
    }

    return render(request, 'products/addcategory.html', context)

@login_required
@admin_only
def update_product(request, product_id):
    instance = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, 'product updated')
            return redirect('/products')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify forms')
            return render(request, 'products/updateproduct.html', {
                'form':form
            })
    context = {
        'form':ProductForm(instance=instance)
    }
    return render(request, 'products/updateproduct.html', context)

@login_required
@admin_only     
def delete_product(request, product_id):
    product = Product.objects.get(id = product_id)
    product.delete()
    messages.add_message(request, messages.SUCCESS,'product deleted')
    return redirect('/products')

@login_required
@admin_only
def update_category(request, category_id):
    instance = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, 'category updated')
            return redirect('/products/category')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify forms')
            return render(request, 'products/updatecategory.html', {
                'form':form
            })
    context = {
        'form':CategoryForm(instance=instance)
    }

    return render(request, 'products/updatecategory.html', context)

@login_required
@admin_only    
def delete_category(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS,'Category deleted')
    return redirect('/products/category')

@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_item_presence = Cart.objects.filter(user=user, product=product)
    if check_item_presence:
        messages.add_message(request, messages.ERROR, 'Item is already present in the cart')
        return redirect('/allproducts') 
    else:
        cart = Cart.objects.create(product=product,user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Product added to cart')
            return redirect('/products/mycart')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add item to cart')

@login_required
def show_cart_item(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items':items
    }
    return render(request,'users/mycart.html', context)

@login_required
def remove_cart_item(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.SUCCESS, 'Item removed from the cart')
    return redirect('/products/mycart')

@login_required
def order_item(request):
    context = {
        'form':OrderForm
    }
    return render(request, 'users/orderform.html', context)