from django.contrib import admin

from images.models import Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = [
        Images.title.field.name,
        Images.slug.field.name,
        Images.image.field.name,
        Images.created.field.name,
    ]
    list_filter = [Images.created.field.name]
