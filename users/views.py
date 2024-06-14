from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import LoginForm
from products.models import *
from .filters import ProductFilter
from django.contrib.auth.decorators import login_required
from . forms import *
from blog.models import *
from django.core.paginator import Paginator

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Account Created')
            return redirect('/register')
        else:
            messages.add_message(request, messages.ERROR, 'Please provide correct details')
            return render(request, 'users/register.html',{
                'form':form
            })
        
    context = {
        'form':UserCreationForm
    }
    return render(request, 'users/register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('/admins/dashboard')
                else:
                    return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'Please provide correct credential')
                return render(request, 'users/login.html', {
                    'form':form
                })
            
    form = LoginForm
    context = {
            'form': form
    }
    return render(request, 'users/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def homepage(request):
    products = Product.objects.all().order_by('-id')[:8]
    blogs = Blog.objects.all().order_by('-id')
    user = request.user.id
    if user:
        items = Cart.objects.filter(user=user)
        context = {
            'products': products,
            'items':items,
            'blogs':blogs
        }
        return render(request, 'users/index.html', context)
    else:
        context = {
                'products': products,
                'blogs':blogs         
        }
        return render(request, 'users/index.html', context)
    
def productspage(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products = Product.objects.all().order_by('-id')
    if min_price and max_price:
        products = Product.objects.filter(product_price__range=(min_price, max_price))
    product_filter = ProductFilter(request.GET, queryset=products)
    product_final = product_filter.qs
    paginator = Paginator(products, 16)  # 16 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_range = range(1, paginator.num_pages + 1)
    user = request.user.id
    if user:
        if request.method == "POST":
            items = Cart.objects.filter(user=user)
            context = {
                'filter': product_filter,
                'items':items,
                'page_obj': page_obj,
                'page_range': page_range
            }
            return render(request,'users/products.html', context)
        else: 
            context = {
                'products': product_final,
                'filter': product_filter,
                'page_obj': page_obj,
                'page_range': page_range
            }
            return render(request, 'users/products.html', context)
    else: 
        context = {
            'products': product_final,
            'filter': product_filter,
            'page_obj': page_obj,
            'page_range': page_range
        }
        return render(request, 'users/products.html', context)

def product_detail(request, product_id):
    products = Product.objects.get(id=product_id)
    product = Product.objects.all().order_by('-id')[:4]
    user = request.user.id
    if user:
        items = Cart.objects.filter(user=user)
        context = {
        'products':products,
        'product':product,
         'items':items
        }
        return render(request, 'users/productdetails.html', context)
    else:
        context = {
                'products':products,
                'product':product
            }
        return render(request, 'users/productdetails.html', context)
            
@login_required
def user_profile(request):
    customer=Customer.objects.all()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "User profile created successfully!")
            return render(request,'layout.html',{
                'customer':customer
            })
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form!')
            return render(request,'users/user_profile.html',{
                'form':form
            })
    
    context = {
        'form':CustomerForm
    }

    return render(request, 'users/user_profile.html', context)
