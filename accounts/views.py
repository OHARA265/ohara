from django.shortcuts import render

from allauth.account.views import SignupView
from app.mixin import SuperuserRequiredMixin
from .forms import CustomSignupForm

# Create your views here.

class SignupView(SignupView,SuperuserRequiredMixin):
        template_name = "account/signup.html"
        form_class = CustomSignupForm