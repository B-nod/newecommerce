from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from users.auth import admin_only

def index(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Form submitted !!")
            return redirect('/services/form')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form !!')
            return render(request,'services/index.html',{
                'form':form
            })
    context = {
        'form':SubmissionForm()
    }
    return render(request, 'services/index.html', context)

@login_required
@admin_only
def services(request):
    services = Submission.objects.all()
    context = {
        'services': services
    }
    return render(request, 'services/show.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Thank you for contacting us.")
            return redirect('/services/contact')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form !!')
            return render(request,'services/contact.html',{
                'form':form
            })
    context = {
        'form':ContactForm()
    }
    return render(request, 'services/contact.html', context)

@login_required
@admin_only
def show_message(request):
    contacts = Contact.objects.all()
    context = {
        'contacts': contacts
    }
    return render(request, 'services/messages.html', context)