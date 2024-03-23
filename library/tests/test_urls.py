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
    
    def test_new_book_resolve(self):
        url = reverse('new_book')
        self.assertEquals(resolve(url).func, NewBook)

    def test_update_book_resolve(self):
        url = reverse('update_book', args=[1])
        self.assertEquals(resolve(url).func, UpdateBook)

    def test_get_all_categories_resolve(self):
        url = reverse('get_all_categories')
        self.assertEquals(resolve(url).func, getAllCategories)

    def test_get_category_info_resolve(self):
        url = reverse('get_category_info')
        self.assertEquals(resolve(url).func, getCategoryInfo)

    def test_upload_book_resolve(self):
        url = reverse('upload_book')
        self.assertEquals(resolve(url).func, UploadBook)

    def test_delete_book_resolve(self):
        url = reverse('delete_book')
        self.assertEquals(resolve(url).func, DeleteBook)

    def test_borrow_book_resolve(self):
        url = reverse('borrow_book')
        self.assertEquals(resolve(url).func, BorrowBook)

    def test_new_category_resolve(self):
        url = reverse('new_category')
        self.assertEquals(resolve(url).func, NewCategory)

    def test_create_new_category_resolve(self):
        url = reverse('createNewCategory')
        self.assertEquals(resolve(url).func, CreateNewCategory)

    def test_all_books_resolve(self):
        url = reverse('all_books')
        self.assertEquals(resolve(url).func, AllBooks)

    def test_get_all_books_resolve(self):
        url = reverse('get_all_books')
        self.assertEquals(resolve(url).func, getAllBooks)

    def test_one_book_resolve(self):
        url = reverse('one_book', args=[1])
        self.assertEquals(resolve(url).func, OneBook)

    def test_all_users_resolve(self):
        url = reverse('all_users')
        self.assertEquals(resolve(url).func, AllUsers)

    def test_get_all_users_resolve(self):
        url = reverse('get_all_users')
        self.assertEquals(resolve(url).func, getAllUsers)

    def test_lib_transactions_resolve(self):
        url = reverse('lib_transactions')
        self.assertEquals(resolve(url).func, LibTransact)

    def test_get_lib_transactions_resolve(self):
        url = reverse('get_lib_transactions')
        self.assertEquals(resolve(url).func, getLibTransactions)

    def test_my_transactions(self):
        url = reverse('member_transactions')
        self.assertEquals(resolve(url).func, MembTransact)

    def test_get_my_transactions(self):
        url = reverse('get_my_transactions')
        self.assertEquals(resolve(url).func, getMyTransactions)

    def test_get_one_transaction(self):
        url = reverse('one_transaction', args=[1])
        self.assertEquals(resolve(url).func, OneTransaction)

    def test_perform_action_on_transaction(self):
        url = reverse('perform_action_on_transaction')
        self.assertEquals(resolve(url).func, PerformActionOnTransaction)
