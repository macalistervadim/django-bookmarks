from http import HTTPStatus

from django.shortcuts import reverse
from django.test import TestCase


class TestHomepage(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse("homepage:homepage"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "homepage/homepage.html")
