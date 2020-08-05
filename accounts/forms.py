# many ways of forming views : model form, class based form
# we will be using model based form

from .models import Order
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


# creating form for model Order

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:  # atleast two field required
        model = Order  # name of model for which form is created
        fields = '__all__'  # for selective fields use python list ['' , '' ]


# import these forms in views.py to work with


class CreateUserForm(UserCreationForm):  # customising default form
    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2']  # these fields name is specified in django documentations
