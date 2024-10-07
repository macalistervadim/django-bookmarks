from django.urls import path

import images.views


app_name = "images"


urlpatterns = [
    path("create/", images.views.image_create, name="create"),
]
