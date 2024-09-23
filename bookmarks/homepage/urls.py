from django.urls import path

import homepage.views


app_name = "homepage"

urlpatterns = [
    path("", homepage.views.HomePageView.as_view(), name="homepage"),
]
