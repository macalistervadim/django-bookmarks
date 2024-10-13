from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import django.shortcuts
from django.test import TestCase

from account.models import Profile
from images.models import Images


class TestDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="password",
        )
        self.profile = Profile.objects.create(
            user=self.user,
        )

        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        self.image = Images.objects.create(
            user=self.user,
            title="Test Image",
            description="Test Description",
            url="https://example.com/image.jpg",
            slug="test-image",
            image=image_file,
        )

    def test_detail_view_valid_data(self):
        self.client.login(username="testuser", password="password")

        url = django.shortcuts.reverse(
            "images:detail",
            kwargs={"id": self.image.id, "slug": self.image.slug},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("image", response.context)
        self.assertEqual(response.context["image"], self.image)
        self.assertEqual(response.context["section"], "images")
        self.assertTemplateUsed(response, "images/image/detail.html")

    def test_detail_view_invalid_data_slug(self):
        self.client.login(username="testuser", password="password")

        url = django.shortcuts.reverse(
            "images:detail",
            kwargs={"id": self.image.id, "slug": "invalid-slug"},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class ImageCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="password",
        )
        self.client.login(username="testuser", password="password")

    def test_create_image_valid_data(self):
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        form_data = {
            "title": "Test Image",
            "description": "Test Description",
            "url": "https://example.com/image.jpg",
            "slug": "test-image",
            "image": image_file,
        }

        response = self.client.post(
            django.shortcuts.reverse("images:create"),
            data=form_data,
        )

        self.assertEqual(Images.objects.count(), 1)
        new_image = Images.objects.first()
        self.assertEqual(new_image.title, "Test Image")
        self.assertEqual(new_image.description, "Test Description")
        self.assertEqual(new_image.url, "https://example.com/image.jpg")
        self.assertEqual(new_image.slug, "test-image")

        self.assertRedirects(response, new_image.get_absolute_url())

    def test_create_image_invalid_data(self):
        form_data = {
            "title": "",
            "description": "Test Description",
            "url": "invalid_url",
            "slug": "test-image",
        }

        self.client.post(
            django.shortcuts.reverse("images:create"),
            data=form_data,
        )

        self.assertEqual(Images.objects.count(), 0)


class TestImageLikeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
        )
        self.client.login(username="testuser", password="testpass")

        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        self.image = Images.objects.create(
            user=self.user,
            title="Test Image",
            description="Test Description",
            url="https://example.com/image.jpg",
            slug="test-image",
            image=image_file,
        )

    def test_like_image(self):
        response = self.client.post(
            django.shortcuts.reverse("images:like"),
            {"id": self.image.id, "action": "like"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
        self.assertIn(self.user, self.image.users_like.all())

    def test_unlike_image(self):
        self.image.users_like.add(self.user)
        response = self.client.post(
            django.shortcuts.reverse("images:like"),
            {"id": self.image.id, "action": "unlike"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
        self.assertNotIn(self.user, self.image.users_like.all())

    def test_like_image_not_authenticated(self):
        self.client.logout()
        response = self.client.post(
            django.shortcuts.reverse("images:like"),
            {"id": self.image.id, "action": "like"},
        )
        self.assertEqual(response.status_code, 302)

    def test_like_non_existing_image(self):
        response = self.client.post(
            django.shortcuts.reverse("images:like"),
            {"id": 9999999999, "action": "like"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Image does not exist"},
        )

    def test_missing_id_or_action(self):
        response = self.client.post(
            django.shortcuts.reverse("images:like"),
            {"action": "like"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Missing image ID or action"},
        )

        response = self.client.post(
            django.shortcuts.reverse("images:like"),
            {"id": self.image.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Missing image ID or action"},
        )


class TestImageListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
        )
        self.profile = Profile.objects.create(
            user=self.user,
        )

        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        self.image = Images.objects.create(
            user=self.user,
            title="Test Image",
            description="Test Description",
            url="https://example.com/image.jpg",
            slug="test-image",
            image=image_file,
        )

    def test_image_list_pagination(self):
        self.client.login(username="testuser", password="testpass")

        for i in range(10):
            Images.objects.create(
                user=self.user,
                title=f"Image {i}",
                description="Test Description",
                url=f"https://example.com/image_{i}.jpg",
                slug=f"image-{i}",
                image=SimpleUploadedFile(
                    f"test_image_{i}.jpg",
                    b"file_content",
                    content_type="image/jpeg",
                ),
            )

        url = django.shortcuts.reverse("images:list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["images"]), 8)

    def test_image_list_view_valid_data(self):
        self.client.login(username="testuser", password="testpass")

        url = django.shortcuts.reverse("images:list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Images.objects.count(), 1)
        self.assertContains(response, "Test Image")

    def test_image_list_view_anonymous_user(self):
        url = django.shortcuts.reverse("images:list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        url_redirect = (
            django.shortcuts.reverse("account:login") + "?next=" + url
        )
        self.assertRedirects(response, url_redirect)
