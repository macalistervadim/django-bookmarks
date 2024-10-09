from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

import account.models
import images.models


class TestImageModel(TestCase):
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

    def test_image_creation_successfully(self):
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )

        image = images.models.Images.objects.create(
            user=self.user,
            title="test",
            url="http://test.com",
            image=image_file,
        )

        self.assertEqual(images.models.Images.objects.count(), 1)
        self.assertEqual(image.title, "test")
        self.assertEqual(image.url, "http://test.com")

        self.assertTrue(image.image.name.startswith("images/"))
        self.assertIn("test_image", image.image.name)

    def test_image_creation_fail(self):
        with self.assertRaises(ValidationError):
            image = images.models.Images(user=self.user, title="", url="")
            image.full_clean()
            image.save()
