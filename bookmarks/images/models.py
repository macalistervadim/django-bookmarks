from typing import Any

from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Images(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]

    def __str__(self) -> models.CharField:
        return self.title

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.user!r}, "
            f"{self.users_like!r}, "
            f"{self.title!r}, "
            f"{self.slug!r}, "
            f"{self.url!r}, "
            f"{self.image!r}, "
            f"{self.description!r}, "
            f"{self.created!r})"
        )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
