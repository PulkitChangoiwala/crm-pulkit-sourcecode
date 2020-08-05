from django.http import HttpResponse
from django.shortcuts import redirect

'''
Decorator is a function is function that takes other function as argument 
and help us to perform action on argument function
'''


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# permission will be different for different users
# so we created two groups for users one is admin and other is customer


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponse("YOU ARE NOT AUTHORIZED TO VIEW THIS PAGE")

        return wrapper_func

    return decorator


#to redirect customer group user to user_page when he clicks on home page url
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer': #this is hardcoded for large number of groups we need to make it dynamic
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
