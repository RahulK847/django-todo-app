from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Task
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(
                username=username,
                password=password
            )

            login(request, user)

            return redirect('home')

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'first_name': request.user.first_name,
        'tasks': tasks
    }
    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')