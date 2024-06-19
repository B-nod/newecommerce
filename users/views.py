from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import LoginForm
from products.models import *
from blog.models import *
from .filters import ProductFilter
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.paginator import Paginator
from django.http import HttpResponse

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save additional user data to UserProfile model
            UserProfile.objects.create(
                user=user,
                dob=form.cleaned_data.get('dob'),
                contact=form.cleaned_data.get('contact'),
                address=form.cleaned_data.get('address')
            )
            messages.add_message(request, messages.SUCCESS, 'Account Created')
            return redirect('/register')
        else:
            messages.add_message(request, messages.ERROR, 'Please provide correct details')
            return render(request, 'users/register.html',{
                'form':form
            })
        
    context = {
        'form':UserRegistrationForm()
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
    if min_price and max_price:
        products = Product.objects.filter(product_price__range=(min_price, max_price))
    else:
        products = Product.objects.all().order_by('-id')
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
    user_profile = UserProfile.objects.get(user=request.user)
    context={
        'user_profile': user_profile
        }
    return render(request, 'templates/layout.html', context)

def recommend_product(request):
    if request.method == 'POST':
        # Get user preferences from form submission
        user_category = request.POST.get('category_name', '')
        min_price = request.POST.get('min_price', '')
        max_price = request.POST.get('max_price', '')
        user_brand = request.POST.get('brand', '')

        # try:
        #     min_price = float(min_price)
        #     max_price = float(max_price)
        # except ValueError:
        #     return HttpResponse("Invalid price format. Please enter valid numbers.")
        
        # Query products based on user preferences
        
        # category = Category.objects.filter(category_name=user_category).first()
        # if category is None or category == '':
        #     # Category exists, perform the query on Product
        #     matched_products = Product.objects.filter(product_price__range=(min_price, max_price), brand=user_brand)

        try:
            category = Category.objects.get(category_name=user_category)
        except Category.DoesNotExist:
            #return HttpResponse("Category does not exist.")
            matched_products = Product.objects.filter(product_price__range=(min_price, max_price), brand=user_brand)
                  
        if min_price is None or max_price is None or min_price == '' or max_price == '':
            matched_products = Product.objects.filter(category__category_name=user_category, brand=user_brand)
        
        elif user_brand is None or user_brand == '':
            matched_products = Product.objects.filter(category__category_name=user_category, product_price__range=(min_price, max_price))

        else:      
            matched_products = Product.objects.filter(category__category_name=user_category, product_price__range=(min_price, max_price), brand=user_brand)
        
        if matched_products.exists():
            context = {
                'matched_products': matched_products,
                'user_category': user_category,
                'min_price': min_price,
                'max_price': max_price
            }
            return render(request, 'users/recommendation.html', context)
        else:
            message = "No matching products found for your preferences. Please try different preferences."
            return HttpResponse(message)
    else:
        # Render initial form template for user input
        return render(request, 'users/preferences_form.html')
    