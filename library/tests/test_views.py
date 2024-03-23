# Testing the views in CatalogPoint

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from library.models import *
import json

class TestViews(TestCase):

    def setUp(self):
        self.librarian_group = Group.objects.create(name='librarian')
        self.member_group = Group.objects.create(name='member')
        self.user = User.objects.create_user(username='testuser',password='testpassword')
        self.client.force_login(self.user)

    def test_sign_up_view_logged_in(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEquals(response.status_code, 302)

    def test_sign_up_view_logged_out(self):
        client = Client()
        response = client.get(reverse('sign_up'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Main/signup.html')

    def test_create_new_user_existing_user(self):
        client = Client()
        create_test_user = User.objects.create_user(username='testuser@gmail.com', email='testuser@gmail.com', password='testpassword')
        created_user_email = create_test_user.email
        password = 'testpassword'
        user_data = {'email': created_user_email, 'password': password}
        response = client.post(reverse('create_new_user'), data=user_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.json(), {'status':'exists'})

    def test_create_user_new_exists_is_false(self):
        client = Client()
        email = 'test@gmail.com'
        password = 'testpassword'
        data = {'email':email, 'password':password}
        response = client.post(reverse('create_new_user'),data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.json(), {'status':'created'})

        
    def test_upper_nav_view(self):
        response = self.client.get(reverse('upper-nav'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Inherit/upper-nav.html')
