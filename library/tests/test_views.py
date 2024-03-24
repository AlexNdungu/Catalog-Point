# Testing the views in CatalogPoint

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from library.models import *
from django.core.files import File
from datetime import datetime, timedelta
import random



class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='librarian')
        Group.objects.create(name='member')
        Cost.objects.create(cost_name='Borrow', cost_description='Test Description', cost_amount=5)

    def setUp(self):
        self.librarian_group = Group.objects.get(name='librarian')
        self.member_group = Group.objects.get(name='member')
        self.user = User.objects.create_user(username='testuser',password='testpassword',email='testuser@gmail.com')
        self.testImage = open('Static/Images/user.jpg', 'rb')
        self.client.force_login(self.user)
        self.category = Category.objects.create(category_name='Test Category', category_description='Test Description')
        self.book = Book.objects.create(book_name='Test Book', book_author='Test Author', book_description='Test Description',
                                        book_category=self.category,book_cover=File(self.testImage))

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

    def test_update_book_user_not_librarian(self):
        self.user.groups.add(self.member_group)
        response = self.client.get(reverse('update_book', args=[self.book.book_id]))
        self.assertEquals(response.status_code, 302)

    def test_update_book_user_librarian(self):
        self.user.groups.add(self.librarian_group)
        response = self.client.get(reverse('update_book', args=[self.book.book_id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/update_book.html')

    def test_get_all_categories(self):
        data = {}
        response = self.client.post(reverse('get_all_categories'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_get_all_category_info(self):
        data = {'category_name':self.category.category_name}
        response = self.client.post(reverse('get_category_info'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_upload_book(self):
        data = {'process':'upload_book','book_title':'Test Book1','book_author':'Test Author',
                'selected_category':self.category.category_name,'book_desc':'Test Description','cover_image':self.testImage,
                'book_copies':5,'book_pages':100}
        
        response = self.client.post(reverse('upload_book'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status':'created'})

    def test_update_book(self):
        data = {'process':'update_book','book_id':self.book.book_id,'book_title':'Test Book Change','book_author':'Test Author',
                'selected_category':self.category.category_name,'book_desc':'Test Description','cover_image':self.testImage,
                'book_copies':5,'book_pages':100}
        
        response = self.client.post(reverse('upload_book'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status':'updated'})

    def test_access_new_category_page_user_not_librarian(self):
        self.user.groups.add(self.member_group)
        response = self.client.get(reverse('new_category'))
        self.assertEquals(response.status_code, 302)

    def test_access_new_category_page_user_librarian(self):
        self.user.groups.add(self.librarian_group)
        response = self.client.get(reverse('new_category'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/new_category.html')

    def test_create_new_category(self):
        # When category exists
        data = {'categ_title':self.category,'categ_description':'Test Description'}
        response = self.client.post(reverse('createNewCategory'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status':'exists'})
        # When category doesn't exist
        data1 = {'categ_title':'Test Category1','categ_description':'Test Description'}
        response1 = self.client.post(reverse('createNewCategory'), data=data1, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response1.json(), {'status':'created'})

    def test_all_books_page(self):
        response = self.client.get(reverse('all_books'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Main/all_books.html')

    def test_get_all_books(self):
        # get all books test
        data = {'category':'all'}
        response = self.client.post(reverse('get_all_books'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        # get all from category empty
        category = Category.objects.create(category_name='Category Not', category_description='Test Description Not')
        data1 = {'category':category.category_name}
        response1 = self.client.post(reverse('get_all_books'), data=data1, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response1.json(), {'status':'empty'})
        # get all from category not empty
        data2 = {'category':self.category.category_name}
        response2 = self.client.post(reverse('get_all_books'), data=data2, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response2.status_code, 200)

    def test_access_one_book_page(self):
        response = self.client.get(reverse('one_book', args=[self.book.book_id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Main/book.html')

    def test_delete_book(self):
        data = {'book_id':self.book.book_id}
        response = self.client.post(reverse('delete_book'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status':'deleted'})

    def test_borrow_book(self):
        # calculate days and cost
        cost = Cost.objects.get(cost_name='Borrow').cost_amount
        max_days = int(500/int(cost))
        borrow_days = random.randint(1, max_days)
        cost_in_days = int(cost * borrow_days)
        from_date = datetime.now().date()
        to_date = from_date + timedelta(days=borrow_days)
        # When books are not available
        data = {'book_id':self.book.book_id,'from_date':from_date,'to_date':to_date,'no_of_days':borrow_days,'cost_in_ksh':cost_in_days}
        response = self.client.post(reverse('borrow_book'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.json(), {'status':'not_available'})
        # When books are available
        self.book.all_copies = 5
        self.book.save()
        response1 = self.client.post(reverse('borrow_book'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response1.json(), {'status':'borrowed'})

    def test_access_all_users_page_not_librarian(self):
        self.user.groups.add(self.member_group)
        response = self.client.get(reverse('all_users'))
        self.assertEquals(response.status_code, 302)

    def test_access_all_users_page_librarian(self):
        self.user.groups.add(self.librarian_group)
        response = self.client.get(reverse('all_users'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/all_users.html')

    def test_get_all_users(self):
        data = {}
        response = self.client.post(reverse('get_all_users'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print(response.json())
        self.assertEquals(response.status_code, 200)
        
        
    def test_upper_nav_view(self):
        response = self.client.get(reverse('upper-nav'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Inherit/upper-nav.html')
