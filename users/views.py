from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetDoneView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.views import View

from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from users.forms import UserRegisterForm, UserForm
from users.models import User
from users.services import add_group, send_registration_mail, check_link, send_reset_password_mail


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        add_group(user)
        send_registration_mail(user)
        return redirect('users:email_confirmation_sent')


class UserConfirmationSentView(PasswordResetDoneView):
    template_name = "users/confirmation/registration_sent_done.html"


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        is_success = check_link(request, uidb64, token)
        if is_success:
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class UserConfirmedView(TemplateView):
    template_name = 'users/confirmation/registration_confirmed.html'


class UserConfirmationFailedView(TemplateView):
    template_name = 'users/confirmation/email_confirmation_failed.html'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        send_reset_password_mail(email)
        return redirect('users:password_reset_done')
    return render(request, 'users/confirmation/password_reset_form.html')


class UserResetDoneView(PasswordResetDoneView):
    template_name = "users/confirmation/password_reset_done.html"
