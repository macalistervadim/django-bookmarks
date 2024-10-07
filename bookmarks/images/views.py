import django.shortcuts
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from images.forms import ImagesCreateForm
from images.models import Images


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImagesCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added successfully")

            return django.shortcuts.redirect(new_image.get_absolute_url())
    else:
        form = ImagesCreateForm(data=request.GET)

    return django.shortcuts.render(
        request,
        "images/image/create.html",
        {"form": form, "section": "images"},
    )


def image_detail(request, id, slug):
    image = django.shortcuts.get_object_or_404(Images, id=id, slug=slug)

    return django.shortcuts.render(
        request,
        "images/image/detail.html",
        {"image": image, "section": "images"},
    )
