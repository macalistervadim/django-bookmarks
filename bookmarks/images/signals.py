from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from images.models import Images

@receiver(m2m_changed, sender=Images.users_like.through)
def users_like_change(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.all().count()
    instance.save()