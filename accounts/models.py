from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from home.models import *
from files.models import *

class CustomUser(AbstractUser):
    pass
    # add additional fields in here
    user_extras = models.ForeignKey('UserExtras', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username

class UserExtras(models.Model):
    id = models.AutoField(primary_key=True)
    profile_photo = models.ForeignKey('files.AppFile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "User Extras"
        verbose_name_plural = "User Extras"


class MailLinkModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    key = models.CharField(max_length=255, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, null=True, blank=True)

    link_type_choices = (
        ('sign_up', 'SignUp'),
        ('reset_password', 'Reset Password'),
    )

    link_type = models.CharField(max_length=100, default="", choices=link_type_choices, null=True, blank=True)

    def __str__(self):
        return self.key


