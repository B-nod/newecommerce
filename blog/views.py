from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.auth import admin_only
from users.filters import BlogFilter

# Create your views here.
@login_required
@admin_only
def add_blog(request):
    if request.method=='POST':
        form=BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Blog added successfully")
            return redirect('/blogs/showblog')
        else:
            messages.add_message(request,messages.ERROR,"Please verify form")
            return render(request,'blogs/addblog.html',{'form':form})
    context={
        'form':BlogForm
    }
    return render(request,'blog/addblog.html',context)

@login_required
@admin_only
def show_blog(request):
    blogs=Blog.objects.all().order_by('-id')
    context={
        'blogs':blogs
    }
    return render(request,'blog/showblog.html',context)

@login_required
@admin_only
def del_blog(request,blog_id):
    blogs=Blog.objects.get(id=blog_id)
    blogs.delete()
    messages.add_message(request,messages.SUCCESS,'Blog deleted')
    return redirect('/blogs/showblog/')

@login_required
@admin_only
def update_blog(request,blog_id):
    instance=Blog.objects.get(id=blog_id)
    if request.method=='POST':
        form=BlogForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Blog updated successfully")
            return redirect('/blogs/showblog')
        else:
            messages.add_message(request,messages.ERROR,"Please verify form")
            return render(request,'blog/updateblog.html',{'form':form})
    context={
        'form':BlogForm(instance=instance)
    }
    return render(request,'blog/updateblog.html',context)

def blogpage(request):
    blogs = Blog.objects.all().order_by('-id')
    blog_filter = BlogFilter(request.GET, queryset=blogs)
    blog_final = blog_filter.qs
    user = request.user.id
    if user:
        if request.method == "POST":
            context = {
                'filter': blog_filter,
            }
            return render(request,'blog/blogs.html', context)
        else: 
            context = {
                'blogs': blog_final,
                'filter': blog_filter,
            }
            return render(request, 'blog/blogs.html', context)
    else: 
        context = {
            'blogs': blog_final,
            'filter': blog_filter,
        }
        return render(request, 'blog/blogs.html', context)


def blog_detail(request, blog_id):
    blogs = Blog.objects.get(id=blog_id)
    blog = Blog.objects.all().order_by('-id')[:3]
    user = request.user.id
    if user:
        context = {
        'blogs':blogs,
        'blog':blog
        }
        return render(request, 'blog/blogdetail.html', context)
    else:
        context = {
                'blogs':blogs,
                'blog':blog
            }
        return render(request, 'blog/blogdetail.html', context)