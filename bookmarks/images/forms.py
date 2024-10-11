from typing import Any

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests

from images.models import Images


class ImagesCreateForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = [
            Images.title.field.name,
            Images.description.field.name,
            Images.url.field.name,
        ]
        widgets = {
            Images.url.field.name: forms.HiddenInput(),
        }

    def clean_url(self) -> Any:
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extensions = url.rsplit(".", 1)[1].lower()
        if extensions not in valid_extensions:
            raise forms.ValidationError(
                "The given URL doest not " "match valid image extensions.",
            )

        return url

    def save(self, force_insert=False, force_update=False, commit=True) -> Any:
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image.url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"

        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)
        if commit:
            image.save()

        return image
