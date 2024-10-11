from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
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


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Images.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Images.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})