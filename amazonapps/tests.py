# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class AppViewTests(TestCase):
    def test_app_index(self):
        """
        A view of the app frontpage
        """
        response = self.client.get(reverse('amazonapps:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post the Amazon app URL here")
