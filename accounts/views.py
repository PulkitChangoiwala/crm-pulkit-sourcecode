from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def registerPage(request):
    '''if request.user.is_authenticated:  # if user is already registers but access register page rediect to home page,
        # we can use middleware so that we do
        # not have to do this thing for every pages
        return redirect('home')
    else:'''
    form = CreateUserForm()  # django provides form for registeration, we can customizze it for ourself
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            '''
            #handling both of theses in signals.py
            # to add recently registered user to group = customer
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            # assigning the customer a user
            Customer.objects.create(
                user=user,
                name=user.username,
            )
            '''
            messages.success(request, 'Account was created for: ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    '''if request.user.is_authenticated:  # if user is already logined but access login page rediect to home page, we can use middleware so that we do
        # not have to do this thing for every pages
        return redirect('home')
    else:'''  # this thing is now handles by @unauthenticated_user from decorators.py

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # django library function login()
            return redirect('home')
        else:
            messages.info(request, 'Username or Password Is Incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')  # for large project we can use middlewares, and put these restriction in single file
@admin_only
def home(request):
    # return HttpResponse("Home Page")
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = Order.objects.filter(status="Delivered").count()
    pending = Order.objects.filter(status="Pending").count()

    context = {"customers": customers, "orders": orders,
               "total_orders": total_orders, "delivered": delivered,
               "pending": pending}
    return render(request, 'accounts/dashboard.html', context)
    # django searcg in accounts -> template -> (accounts -> dashboard.html)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'orders': orders, "total_orders": total_orders, "delivered": delivered,
               "pending": pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        #request.FILES for photo or other file submissions in the form
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    # in context dictionary first name (key value) is the name we gonna use in template and second is value(list
    # variable in this file)
    return render(request, 'accounts/products.html', {"products": products})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk_customer):
    customer = Customer.objects.get(id=pk_customer)
    orders = customer.order_set.all()
    order_count = orders.count()

    # filter search using django_filter library
    # create filters.py (it will look similar to forms.py}
    # update in customer.html to render filter form
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {"customer": customer,
               "orders": orders,
               "order_count": order_count, 'myfilter': myfilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)

    '''
    #formset is used because we have one to many relationship from Customer to Order and for each customer we want to place
    #multiple order together
    '''

    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    ''''
    # form by default has request.method == GET
    # but when we submit the form it will redirect(Post) to the same url thus this same
    # view. Hence second time request.method is POST with request.POST containing the
    # form data
    
    '''
    if request.method == 'POST':
        # form = OrderForm(request.POST)  # loading POST data
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()  # saving values in model
            return redirect('/')  # after one post method return to base url

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)  # prefilling the form for update

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # loading POST data, instance is passed
        # so that new data is stored in the instance, no new entry will be created
        if form.is_valid():
            form.save()  # saving values in model
            return redirect('/')  # after one post method return to base url

    context = {'form': form}
    return render(request, 'accounts/update_order_form.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
