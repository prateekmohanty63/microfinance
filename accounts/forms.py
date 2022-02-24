from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.conf import settings
from .models import *
from .utils import *


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control py-3 mb-3', 'placeholder': 'Email'}
        )
        )
    password = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control py-3 mb-3', 'placeholder': 'Password', 'autocomplete': 'off', 'data-toggle': 'password'}
        )
    )

    def clean(self):
        email = self.cleaned_data.get('email').lower()
        password = self.cleaned_data.get('password')
        if CustomUser.objects.filter(email=email).exists() is False:
            raise ValidationError("Email does not exist! Please create an account before logging in.")
        else:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password) is False:
                raise ValidationError("Invalid Password")
            else:
                if user.is_active is False:
                    raise ValidationError("You are not an active user, please confirm your email first or contact to support")
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('The password and confirm password fields didn’t match.'),
    }

    first_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class':'form-control py-3 mb-3',
                'placeholder': 'Name'
                }
            ),
        label="",
        )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control py-3 mb-3',
                'placeholder': 'Email'
                }
            ),
        label="",
        )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                 'placeholder': 'Password',
                 'class': 'form-control py-3 mb-3 signup-pswrd',
                 },
            ),
        label="",
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Confirm password',
                'class': 'form-control py-3 mb-3 signup-pswrd',
                }
            ),
        label="",
        )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean(self):
       email = self.cleaned_data.get('email').lower()
       if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email is already exists, please use unique email address")
       return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data.get('email').lower()
        user.is_active = False
        if commit:
            user.save()
        return user


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control py-3 mb-3', 'placeholder': 'Your email'}
        )
        )

    class Meta:
        model = CustomUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'New password',
            'class': 'form-control py-3 mb-3 signup-pswrd',
            }),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label="",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Confirm new password',
            'class': 'form-control py-3 mb-3 signup-pswrd',
            }),
    )
