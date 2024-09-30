from django.urls import include, path

import account.views


app_name = "account"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("login/", account.views.UserLoginView.as_view(), name="login"),
    path(
        "password-change/",
        account.views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-reset/",
        account.views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        account.views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("", account.views.DashboardView.as_view(), name="dashboard"),
    path("register/", account.views.RegisterView.as_view(), name="register"),
    path("edit/", account.views.EditView.as_view(), name="edit"),
]
