import datetime
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from actions.models import Action


def create_action(user: Any, verb: str, target: Any = None) -> bool:
    now = timezone.now()
    last_minute = now - datetime.timedelta(minutes=1)
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb=verb,
        created__gte=last_minute,
    )

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id,
        )

    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True

    return False
