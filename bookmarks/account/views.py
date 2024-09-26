from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import django.shortcuts
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

import account.forms


class UserLoginView(FormView):
    template_name = "account/login.html"
    form_class = account.forms.LoginForm

    def form_valid(self, form) -> HttpResponse:
        cd = form.cleaned_data
        user = authenticate(
            username=cd["username"],
            password=cd["password"],
        )

        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponse("Logged in successfully")
            else:
                return HttpResponse("Your account is disabled")
        else:
            return HttpResponse("Invalid login or password")


class RegisterView(FormView):
    template_name = "account/register.html"
    form_class = account.forms.UserRegistrationForm

    def form_valid(self, form) -> HttpResponse:
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()

        return django.shortcuts.render(
            self.request,
            "account/register_done.html",
            {"new_user": new_user},
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user_form"] = self.get_form()
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["section"] = "dashboard"

        return context


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")


class CustomPasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("account:password_reset_done")


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")
