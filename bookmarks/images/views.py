from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
import django.shortcuts
from django.views import View
from django.views.generic import CreateView, DetailView

from images.forms import ImagesCreateForm
from images.models import Images


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Images
    form_class = ImagesCreateForm
    template_name = "images/image/create.html"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial.update(self.request.GET.dict())
        return initial

    def form_valid(self, form: ImagesCreateForm) -> HttpResponse:
        form.instance.user = self.request.user
        messages.success(self.request, "Image added successfully")
        return super().form_valid(form)

    def form_invalid(self, form: ImagesCreateForm) -> HttpResponse:
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["section"] = "images"
        return context


class ImageDetailView(DetailView):
    model = Images
    template_name = "images/image/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["image"] = self.object
        context["section"] = "images"

        return context


class ImageLikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest) -> HttpResponse:
        image_id = request.POST.get("id")
        action = request.POST.get("action")

        if not image_id or not action:
            return JsonResponse(
                {"status": "error", "message": "Missing image ID or action"},
            )

        try:
            image = Images.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
            elif action == "unlike":
                image.users_like.remove(request.user)
            else:
                return JsonResponse(
                    {"status": "error", "message": "Invalid action"},
                )

            return JsonResponse({"status": "ok"})
        except Images.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Image does not exist"},
            )


@login_required
def image_list(request: HttpRequest) -> HttpResponse:
    images = Images.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)

    if images_only:
        return django.shortcuts.render(
            request,
            "images/image/list_images.html",
            {"section": "images", "images": images},
        )

    return django.shortcuts.render(
        request,
        "images/image/list.html",
        {"section": "images", "images": images},
    )
