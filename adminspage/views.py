from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.auth import admin_only


@login_required
@admin_only
def admin_home(request):
    return render(request, 'admins/adminhome.html')
