from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['section'] = 'login'
        return context

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if not user:
            context = self.get_context_data(form=form)
            context['invalid'] = True
            return self.render_to_response(context)

        login(self.request, user)
        return HttpResponseRedirect(reverse('dashboard'))
