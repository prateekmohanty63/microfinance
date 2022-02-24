from django.db.models.signals import post_save
from .models import *

def initUser(sender, instance, **kwargs):

    if kwargs['created']:

        # Stuff for first time user sign up
        email = instance.username.lower()
        instance.username = email # Override username to be email
        instance.email = email
        instance.save()
        
        # Create the user extras record for storing attributes
        user_extras = UserExtras()
        user_extras.user = instance
        user_extras.save()

        instance.user_extras = user_extras
        instance.save()

post_save.connect(initUser, sender=CustomUser)