from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
import django.shortcuts
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    View,
)

import account.forms
import account.models


class UserLoginView(FormView):
    template_name = "account/login.html"
    form_class = account.forms.LoginForm

    def form_valid(self, form: account.forms.LoginForm) -> HttpResponse:
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

    def form_valid(
        self,
        form: account.forms.UserRegistrationForm,
    ) -> HttpResponse:
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()
        account.models.Profile.objects.create(user=new_user)

        return django.shortcuts.render(
            self.request,
            "account/register_done.html",
            {"new_user": new_user},
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user_form"] = self.get_form()
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["section"] = "dashboard"

        return context


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")


class CustomPasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("account:password_reset_done")


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")


class EditView(LoginRequiredMixin, FormView):
    template_name = "account/edit.html"
    form_class = account.forms.UserEditForm
    profile_form_class = account.forms.ProfileEditForm
    success_url = reverse_lazy("account:edit")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["profile_form"] = self.profile_form_class(
            instance=self.request.user.profile,
        )
        return context

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        user_form = self.get_form()
        profile_form = self.profile_form_class(
            data=request.POST,
            files=request.FILES,
            instance=request.user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
            return django.shortcuts.redirect(self.get_success_url())
        else:
            messages.error(request, "Error updating profile")
            return self.form_invalid(user_form)

    def get_form(self, form_class: Any = None) -> Any:
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(
            instance=self.request.user,
            data=self.request.POST or None,
        )

    def form_invalid(
        self,
        form: account.forms.UserEditForm,
    ) -> TemplateResponse:
        context = self.get_context_data(form=form)
        context["profile_form"] = self.profile_form_class(
            instance=self.request.user.profile,
        )
        return self.render_to_response(context)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "account/user/list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["section"] = "people"
        context["users"] = self.get_queryset()
        return context

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "account/user/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["section"] = "people"

        return context

    def get_object(self, queryset: Any = None) -> Any:
        username = self.kwargs.get("username")
        user = User.objects.get(username=username, is_active=True)

        return user


class UserFollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> JsonResponse:
        user_id = request.POST.get("id")
        action = request.POST.get("action")
        if user_id and action:
            user = django.shortcuts.get_object_or_404(User, id=user_id)
            if action == "follow":
                account.models.Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user,
                )
            else:
                account.models.Contact.objects.filter(
                    user_from=request.user,
                    user_to=user,
                ).delete()
            return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "error"})
