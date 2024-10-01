from typing import Any

from django.contrib.auth.models import User
from django.http import HttpRequest

import account.models


class EmailAuthBackend:
    """
    Аутентифицировать посредством эл. почты
    """

    def authenticate(
        self,
        request: HttpRequest,
        username: str | None = None,
        password: str | None = None,
    ) -> User | None:
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int) -> User | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(
    backend: Any,
    user: User,
    *args: Any,
    **kwargs: Any,
) -> None:
    """
    Создать профиль пользователя для социальной аутентификации
    """
    if not account.models.Profile.objects.filter(user=user).exists():
        account.models.Profile.objects.create(user=user)
