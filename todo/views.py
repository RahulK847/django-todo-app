from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def base(request):
    return render(request, 'base.html', {
        'naam': 'Django'})

def home(request):
    context = {
        'name': 'Rahul',
    }
    return render(request, 'home.html', context)
