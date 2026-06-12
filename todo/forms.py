from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import ModelForm, ValidationError
from .models import Task


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(required=True) # Add first_name field
    last_name = forms.CharField(required=True) # Add last_name field
    email = forms.EmailField(required=True) # Add email field

    class Meta:
        # Define the model and fields to be used in the form
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
    def clean_email(self):
        # Check if email already exists
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name']   # only these two — username/email locked
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True

class TaskForm(ModelForm): # Define a form for the Task model

    class Meta: # Define the model and fields to be used in the form
        model = Task
        fields = ['title', 'priority', 'deadline'] # Define the fields to be used in the form
        
        widgets = { # Use a DateTimeInput widget for the deadline field to allow users to select date and time
        'deadline': forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    }

    def __init__(self, *args, **kwargs): # Override the __init__ method to set priority field as optional
        super().__init__(*args, **kwargs) # Call the parent class's __init__ method
        self.fields['priority'].required = False
        self.fields['deadline'].required = False

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password1")

        if old_password and new_password and old_password == new_password:
            raise ValidationError("New password cannot be the same as the old password.")

        return new_password