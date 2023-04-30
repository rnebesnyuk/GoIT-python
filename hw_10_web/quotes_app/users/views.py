from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib import messages
from django.urls import reverse_lazy

from quotes.utils import DataMixin

from .forms import *


# Create your views here.
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data["username"]
        messages.success(
            self.request, f"Welcome, {username}. Your account has been registered!"
        )
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("home")


def logout_user(request):
    logout(request)
    return redirect("home")
