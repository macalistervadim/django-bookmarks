from django.urls import path

import images.views


app_name = "images"


urlpatterns = [
    path("create/", images.views.ImageCreateView.as_view(), name="create"),
    path(
        "detail/<int:id>/<slug:slug>/",
        images.views.ImageDetailView.as_view(),
        name="detail",
    ),
    path("like/", images.views.ImageLikeView.as_view(), name="like"),
    path("", images.views.image_list, name="list"),
]
