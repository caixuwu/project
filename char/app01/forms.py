from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

class User(UserCreationForm):
