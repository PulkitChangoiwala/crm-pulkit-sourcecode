from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer


# oveerride apps.py 's ready function
# and change INSTALLED_APPS  in setting.py
# signals are more dynamic way of creating profiles
# even if we create user from admin, signal will create corresponding profile

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name=instance.username,
        )
        print('profile created')


post_save.connect(customer_profile, sender=User)  # whenever user is saved call this signal
