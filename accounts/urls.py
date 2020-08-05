from django.urls import path
from .views import *
urlpatterns = [

    path('register/', registerPage, name = "register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),

    path('', home, name = 'home'),  # name can be used in templates, we donot need to hard code urls there
    path('user/', userPage, name="user-page"),

    path('account/', accountSettings, name="account"),

    path('products/', products, name="products"),
    path('customer/<str:pk_customer>', customer, name="customer"), #making url dynamic

    path('create_order/<str:pk>', createOrder, name = "create_order"),
    path('update_order/<str:pk>', updateOrder, name="update_order"),
    path('delete_order/<str:pk>', deleteOrder, name="delete_order"),
]
