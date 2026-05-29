from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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