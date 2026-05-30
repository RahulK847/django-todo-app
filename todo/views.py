from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Task
from .forms import RegisterForm, TaskForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup_view(request):
    form = RegisterForm() # Initialize the form outside the if block so that it can be used in both GET and POST requests

    if request.method == 'POST':
        form = RegisterForm(request.POST) # Create a form instance with the submitted data

        if form.is_valid():
            user = form.save()  

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(    # Authenticate the user using the provided username and password
                username=username,
                password=password
            )

            login(request, user) # Log the user in and create a session for them

            return redirect('home')

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated: # If the user is already authenticated, redirect them to the home page
        return redirect('home')
    
    form = AuthenticationForm() # Initialize the form outside the if block so that it can be used in both GET and POST requests

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # Create a form instance with the submitted data and the request object (required for AuthenticationForm)

        if form.is_valid():
            user = form.get_user()
            login(request, user) # Log the user in and create a session for them
            return redirect('home')
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    form = TaskForm() # Initialize the form to be used in the template for adding new tasks
    tasks = Task.objects.filter(user=request.user)
    context = {
        'first_name': request.user.first_name,
        'tasks': tasks,
        'form': form
    }
    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def add_task(request):
    if request.method == "POST":
        form  = TaskForm(data=request.POST)
        print("post request received")

        if form.is_valid():
            print("form is valid")
            task = form.save(commit=False) # Create a Task object but don't save it to the database yet
            task.user = request.user # Set the user field of the Task object to the currently logged-in user
            task.save() # Now save the Task object to the database
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = TaskForm()
    return render(request, 'home.html', {'form': form})
        

