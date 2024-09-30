from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self.user!r}, "
            f"{self.date_of_birth!r}, "
            f"{self.photo!r})"
        )