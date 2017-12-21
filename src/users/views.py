from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView

from users.forms import LoginForm, SignupForm


class LoginView(LoginView):

    redirect_authenticated_user = True
    template_name = 'login_form.html'


class LogoutView(LogoutView):
    pass
    # template_name = 'logged_out.html'


class SignupView(FormView):

    form_class = SignupForm
    template_name = 'signup_form.html'
