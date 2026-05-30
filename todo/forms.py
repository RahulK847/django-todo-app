from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
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

class TaskForm(ModelForm):

    # priority_choices = [
    #     (0, 'High'),
    #     (1, 'Normal'),
    #     (2, 'Low'),
    # ]
    # priority = forms.ChoiceField(required=False, initial=1, choices=priority_choices, widget=forms.Select())
    # we don't need to define priority field here as it is already defined in the model with choices, we can directly use it in the form

    deadline = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    # unlike priority, we need to define deadline field here because we want to use a custom widget for it, and also make it optional

    class Meta:
        model = Task
        fields = ['title']