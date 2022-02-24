from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import *
from .models import *

from messaging.tasks import send_email
from .utils import create_link

from django.conf import settings
from django.contrib.auth import authenticate, login

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = LoginForm()
            return render(request, self.template_name, locals())

    def post(self, request):
        form = LoginForm(request.POST)
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        if form.is_valid():
            user = get_object_or_404(CustomUser, email=email)
            auth_obj = authenticate(request=request, username=user.username, password=password)
            if auth_obj:
                login(request, auth_obj)
                return redirect('home')
        else:
            return render(request, self.template_name, locals())


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():

            # Save the new user
            user = form.save()
            user_email = user.email
            user_name = user.get_full_name()
            
            # Create a verification link to confirm their email
            link, key = create_link(link_for='sign-up')
            obj, created = MailLinkModel.objects.update_or_create(user=user, link_type="sign_up", is_delete=False)
            obj.key = key
            obj.save()

            # Send email out using celery
            send_email.delay(recipient_name=user_name, link=link, recipient_list=user_email, subject="Complete Microfinance Sign Up", mail_for="sign-up")

            context = {'email': user_email, 'render_kind': 'signup'}

            return render(request, 'confirm-page.html', context)
        
        else:
            return render(request, 'register.html', locals())


class VerifyUserLinkView(View):
    def get(self, request):

        get_key = request.GET.get('key')
        link_obj = get_object_or_404(MailLinkModel, key=get_key)

        if link_obj:
            #if link_obj.is_delete is False:
            user = get_object_or_404(CustomUser, pk=link_obj.user_id)
            
            if link_obj.link_type == 'sign_up':
                
                user.is_active = True
                user.save()
                link_obj.is_delete = True
                link_obj.save()

                user_name = user.get_full_name()
                return render(request, 'confirm-page.html', {'render_kind': 'signup_confirmed'})

            elif link_obj.link_type == 'reset_password':

                request.session['forgot_password_user_pk'] = user.pk
                request.session['forgot_password_link_pk'] = link_obj.pk
                return redirect('create_new_password')

        return render(request, 'confirm-page.html', {'render_kind': 'invalid_key'})


class ResetPasswordView(View):
    template_name = 'reset-password-request.html'

    def get(self, request):
        form = UserPasswordResetForm()
        return render(request, self.template_name, locals())

    def post(self, request):
        email = request.POST.get('email')
        user = get_object_or_404(CustomUser, email=email)

        if user:
            if user.is_active:
                user_email = user.email
                user_name = user.get_full_name()

                # Create a link for verification and assign it to reset_password type
                link, key = create_link(link_for='reset-password')
                obj, created = MailLinkModel.objects.update_or_create(user=user, link_type="reset_password", is_delete=False)
                obj.key = key
                obj.save()

                # Send email out using celery
                send_email.delay(recipient_name=user_name, link=link, recipient_list=user_email, subject="Reset your Microfinance password", mail_for="reset-password")
                
                context = {'email': user_email, 'render_kind': 'reset_password'}

                return render(request, 'confirm-page.html', context)

        return self.get(request)


class CreateNewPasswordView(View):
    template_name = 'reset-password-confirm.html'

    def get(self, request):
        user_pk = request.session.get('forgot_password_user_pk')
        user = get_object_or_404(CustomUser, pk=user_pk)
        form = UserSetPasswordForm(user=user)
        return render(request, self.template_name, locals())

    def post(self, request):
        user_pk = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_pk)
        form = UserSetPasswordForm(data=request.POST, user=user)

        if form.is_valid():
            form.save()
            request.session.pop('forgot_password_user_pk')
            link_obj_pk = request.session.get('forgot_password_link_pk')
            link_obj = get_object_or_404(MailLinkModel, pk=link_obj_pk)
            link_obj.is_delete = True
            link_obj.save()
            request.session.pop('forgot_password_link_pk')

            user_email = user.email
            user_name = user.get_full_name()

            # Send email out using celery
            send_email.delay(recipient_name=user_name, link='', recipient_list=user_email, subject="Your Microfinance Password Was Changed", mail_for="password-change")

            return render(request, 'confirm-page.html', {'render_kind': 'password_updated'})

        else:
            return render(request, self.template_name, locals())
