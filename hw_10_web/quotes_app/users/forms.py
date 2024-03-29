from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input"}), required=False)
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(label="Repeat password",
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "password1": "Password",
            "password2": "Repeat password",
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
