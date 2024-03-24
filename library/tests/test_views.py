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
        self.user = User.objects.create_user(username='testuser',password='testpassword',email='testuser@gmail.com')
        self.testImage = open('Static/Images/user.jpg', 'rb')
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
        email = self.user.email
        user_data = {'email': email}
        response = client.post(reverse('create_new_user'), data=user_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.json(), {'status':'exists'})

    def test_create_user_new_exists_is_false(self):
        client = Client()
        email = 'test@gmail.com'
        data = {'email':email}
        response = client.post(reverse('create_new_user'),data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.json(), {'status':'created'})

    def test_sign_in_logged_in(self):
        response = self.client.get(reverse('signin'))
        self.assertEquals(response.status_code, 302)

    def test_sign_in_logged_out(self):
        client = Client()
        response = client.get(reverse('signin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Main/signin.html')

    def test_logout(self):
        response = self.client.get(reverse('signout'))
        self.assertEquals(response.status_code, 302)

    def test_sign_in_user_user_doesnt_exist(self):
        client = Client()
        email = 'usernot@gmail.com'
        data = {'email':email}
        response = client.post(reverse('signin_user'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.json(), {'status':'not_found'})

    def test_sign_in_user_wrong_password(self):
        client = Client()
        new_user = User.objects.create_user(username='newuser',password='newpassword',email='newuser@gmail')
        email = new_user.email
        wrong_password = 'wrongpassword'
        data = {'email':email, 'password':wrong_password}
        response = client.post(reverse('signin_user'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.json(), {'status':'wrong_password'})

    def test_sign_in_user_correct_password(self):
        client = Client()
        new_user = User.objects.create_user(username='newuser',password='newpassword',email='newuser@gmail')
        email = new_user.email
        password = 'newpassword'
        data = {'email':email, 'password':password}
        response = client.post(reverse('signin_user'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.json(), {'status':'found'})

    # This is an example for all the views with the wrapper @login_required
    def test_access_profile_logged_out(self):
        client = Client()
        response = client.get(reverse('profile'))
        self.assertEquals(response.status_code, 302)

    def test_access_profile_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Main/profile.html')

    def test_access_one_user_not_librarian(self):
        self.user.groups.add(self.member_group)
        response = self.client.get(reverse('one_user', args=[self.user.username]))
        self.assertEquals(response.status_code, 302)

    def test_access_one_user_librarian(self):
        self.user.groups.add(self.librarian_group)
        response = self.client.get(reverse('one_user', args=[self.user.username]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/user.html')

    def test_update_profile_add_and_remove_profilePicture(self):
        # First add a profile picture
        data = {'to_update':'profile_pic','profile_pic':self.testImage}
        response = self.client.post(reverse('update_profile'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        # Then remove the profile picture
        data1 = {'to_update':'remove_profile_pic'}
        response1 = self.client.post(reverse('update_profile'), data=data1, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response1.json(), {'message':'suceess'})

    def test_update_profile_bio(self):
        data = {'to_update':'bio','bio':'This is a test bio'}
        response = self.client.post(reverse('update_profile'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_update_profile_all_details(self):
        data = {'to_update':'all_details','fullname':'Test User','secondary_email':'test@gmail.com',
                'website':'www.test.com','location':'Test Location','company':'Test Company'}  
        response = self.client.post(reverse('update_profile'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_delete_user(self):
        data = {'username':self.user.username}
        response = self.client.post(reverse('delete_user'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status':'deleted'})

    def test_access_new_book_page_user_not_librarian(self):
        self.user.groups.add(self.member_group)
        response = self.client.get(reverse('new_book'))
        self.assertEquals(response.status_code, 302)

    def test_access_new_book_page_user_librarian(self):
        self.user.groups.add(self.librarian_group)
        response = self.client.get(reverse('new_book'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/new_book.html')
        
    def test_upper_nav_view(self):
        response = self.client.get(reverse('upper-nav'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Inherit/upper-nav.html')
