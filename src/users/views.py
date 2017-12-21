from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
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
    success_url = settings.LOGIN_REDIRECT_URL  # reverse_lazy('home_page')

    def form_valid(self, form):
        """
        Además de crear el usuario, iniciamos sesión con el usuario recién creado
        """
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)
