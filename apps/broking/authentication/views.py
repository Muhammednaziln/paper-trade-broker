from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as CoreLoginView
from django.utils.datetime_safe import date
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView

from apps.broking.authentication.models import AuthSession
from apps.users.forms import UserCreationForm
from apps.users.models import TradeApp


class LoginView(CoreLoginView):
    """
    For public login, we expect to have an 'api_key' and optionally a 'state' and a 'redirect_to'.
    If there is an api key, then the successful login will get redirected to the
    """
    redirect_authenticated_user = 1

    trade_app = False         # using ellipses instead of None.

    def get_trade_app(self):
        if self.trade_app is False:
            access_key = self.request.GET.get('api_key')
            if access_key:
                self.trade_app = TradeApp.objects.filter(access_key=access_key).first()
        return self.trade_app

    def get_success_url(self):
        trade_app = self.get_trade_app()
        if trade_app:

            # create session against user.
            # reusing auth session if available as it is just a moke platform.
            session = AuthSession.objects.filter(app=trade_app, user=self.request.user, created_at__contains=date.today(), is_active=True).last()
            if session is None:
                session = AuthSession(app=trade_app, user=self.request.user)
                session.save()

            redirect_url = self.request.GET.get('redirect_to', self.get_trade_app().redirect_url or 'http://localhost:8000/callback/')
            redirect_url += "?userid=" + self.request.user.username

            # reusing assigned access_token is not a secure way. still this is just a moke platform
            # always better to take this access toke to generate a JWT.
            redirect_url += "&access_token=" + session.access_token
            redirect_url += "&state=" + self.request.GET.get('state', '')
            return redirect_url
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        kwargs['trade_app'] = self.get_trade_app()
        return super().get_context_data(**kwargs)

class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}!')
        login(self.request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)

