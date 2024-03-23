# Testing the views in CatalogPoint

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from library.models import *

class TestViews(TestCase):

    def setUp(self):
        self.librarian_group = Group.objects.create(name='librarian')
        self.member_group = Group.objects.create(name='member')
        self.user = User.objects.create_user(username='testuser',password='testpassword')

    def test_upper_nav_view(self):
        client = Client()
        response = client.get(reverse('upper-nav'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Inherit/upper-nav.html')
