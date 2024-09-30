from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

import account.models


class TestProfileModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test",
            email="mail@mail.ru",
            password="testpassword",
        )
        self.profile = account.models.Profile.objects.create(
            user=self.user,
            date_of_birth=date(1900, 1, 1),
        )

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, account.models.Profile))
        self.assertEqual(self.profile.user.username, "test")
        self.assertEqual(self.profile.user.email, "mail@mail.ru")
        self.assertEqual(self.profile.date_of_birth, date(1900, 1, 1))
