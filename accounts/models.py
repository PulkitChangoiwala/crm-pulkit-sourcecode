from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#all created models must be registered in admin.py

#one to many relationship between customer to order
#many to many relationship. eg: Product Tags and Product. We need an intermediatery tag to implement it

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) #linking user with customer
    name = models.CharField(max_length=200,
                            null=True)  # null = True, allows enter a data of customer with this field null
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):  # customer is referred with self.name
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200,
                            null=True)

    def __str__(self):  # customer is referred with self.name
        return self.name



class Product(models.Model):
    CATEGORY = (                    # dropdown menu
        ('Social Media', 'Social Media'),
        ('E-Commerce', 'E-Commerce'),
        ('E-Payment', 'E-Payment'),
        ('Telecom', 'Telecom'),
        ('Video Streaming', 'Video Streaming'),
        ('E-Reader', 'E-Reader'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY) #dropdown menu
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):  # product is referred with self.name
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('In Talk', 'In Talk'),
        ('Delivered', 'Delivered'),
    )
    # customer to orders is one to many relationship
    # product to order is one to many relationship
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) #Customer is parent model
    product = models.ForeignKey(Product, null = True, on_delete= models.SET_NULL) #Product is parent model
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    def __str__(self):  # product is referred with self.name
        return self.product.name
