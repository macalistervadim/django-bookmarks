from django.contrib import admin

from actions.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        Action.verb.field.name,
        "target",
        "created",
    ]
    list_filter = [Action.created.field.name]
    search_fields = [Action.verb.field.name]
