from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, TaskHistory
from .forms import RegisterForm, TaskForm, UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.utils import timezone


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
    sort_cycle = {
        "date": "priority",
        "priority": "deadline",
        "deadline": "date"
    }

    form = TaskForm() # Initialize the form to be used in the template for adding new tasks

    current_sort = request.GET.get('sort', 'date') # Get the current sorting criteria from the query parameters, default to 'date' if not provided
    
    if current_sort not in sort_cycle:
        current_sort = 'date' # If the provided sorting criteria is not valid, default to 'date'

    next_sort = sort_cycle[current_sort] # Get the next sorting criteria for the toggle button in the template
    
    if current_sort == 'date':
        tasks = Task.objects.filter(user=request.user).order_by('-created_at') # Sort tasks by creation date in descending order'
    elif current_sort == 'priority':
        tasks = Task.objects.filter(user=request.user).order_by('priority') # Sort tasks by priority in ascending order
    elif current_sort == 'deadline':
        tasks = Task.objects.filter(user=request.user).order_by(F('deadline').asc(nulls_last=True)) # Sort tasks by deadline in ascending order
    
    context = {
        'first_name': request.user.first_name,
        'tasks': tasks,
        'form': form,
        'current_sort': current_sort,
        'next_sort': next_sort,
        'now': timezone.now(), # Pass the current time to the template for deadline comparison
    }
    return render(request, 'home.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

def add_task(request):
    if request.method == "POST":
        form  = TaskForm(data=request.POST)
        # print("post request received")

        if form.is_valid():
            print("form is valid")
            task = form.save(commit=False) # Create a Task object but don't save it to the database yet
            task.user = request.user # Set the user field of the Task object to the currently logged-in user
            task.save() # Now save the Task object to the database
            return redirect('home')
        # else:
        #     print(form.errors)
    else:
        form = TaskForm()
    return render(request, 'home.html', {'form': form})

@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    TaskHistory.objects.create(
        user = request.user, 
        title = task.title, 
        action = TaskHistory.COMPLETED
        )
    task.delete()
    return redirect('home')

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    TaskHistory.objects.create(
        user = request.user, 
        title = task.title, 
        action = TaskHistory.DELETED
        )
    task.delete()
    return redirect('home')

def task_history(request):
    history = TaskHistory.objects.filter(user=request.user)
    return render(request, 'history.html', {'history': history})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})
        

