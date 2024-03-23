# Testing the urls in CatalogPoint
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from library.views import *

class TestUrls(SimpleTestCase):

    def test_signup_resolve(self):
        url = reverse('sign_up')
        self.assertEquals(resolve(url).func, signUp)

    def test_create_new_user_resolve(self):
        url = reverse('create_new_user')
        self.assertEquals(resolve(url).func, createNewUser)

    def test_signin_resolve(self):
        url = reverse('signin')
        self.assertEquals(resolve(url).func, signIn)

    def test_signin_user_resolve(self):
        url = reverse('signin_user')
        self.assertEquals(resolve(url).func, signInUser)

    def test_signout_resolve(self):
        url = reverse('signout')
        self.assertEquals(resolve(url).func, signOut)

    def test_upper_nav_resolve(self):
        url = reverse('upper-nav')
        self.assertEquals(resolve(url).func, UpperNav)

    def test_profile_resolve(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, Profile)

    def test_one_user_resolve(self):
        url = reverse('one_user', args=['user'])
        self.assertEquals(resolve(url).func, OneUser)

    def test_update_profile_resolve(self):
        url = reverse('update_profile')
        self.assertEquals(resolve(url).func, UpdateProfile)

    def test_delete_user_resolve(self):
        url = reverse('delete_user')
        self.assertEquals(resolve(url).func, DeleteUser)