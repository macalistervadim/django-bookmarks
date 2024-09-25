from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import django.shortcuts
from django.urls import reverse_lazy
from django.views.generic import TemplateView

import account.forms


def user_login(request):
    if request.method == "POST":
        form = account.forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd["username"],
                password=cd["password"],
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Logged in successfully")
                else:
                    return HttpResponse("Your account is disabled")
            else:
                return HttpResponse("Invalid login or password")
    else:
        form = account.forms.LoginForm()

    return django.shortcuts.render(
        request=request,
        template_name="account/login.html",
        context={"form": form},
    )


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
