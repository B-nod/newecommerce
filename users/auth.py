from django.shortcuts import redirect

#to check if the user is logged in or not 
# Decorators:
# 1. `unauthenticated_user`: 
#    This decorator ensures that if a user is already authenticated (logged in), 
#    they are redirected to the homepage (`'/'`) and cannot access the view 
#    decorated with it (e.g., the login page).
#    If the user is not authenticated, the original view is executed.
#
# 2. `admin_only`: 
#    This decorator restricts access to the view only to users who are staff 
#    (i.e., admins). If a normal user tries to access the view, they are 
#    redirected to the homepage (`'/'`). Only admins can see the content of 
#    the view decorated with `@admin_only`.
#
# Example usage in Django views:

def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_function(request, *args, **kwargs)
        
    return wrapper_function

#give access to admin pages if request comes from admin
# if request is from normal user, redirect to user dashboard

def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_function

