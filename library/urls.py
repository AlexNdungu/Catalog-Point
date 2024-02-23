from django.urls import path
from . import views

urlpatterns = [

    # Sign up url
    path('',views.signUp, name='sign_up'),

    # Create new user
    path('createNewUser/', views.createNewUser, name='create_new_user'),

    # Sign in url
    path('signin/',views.signIn, name='signin'),

    # Sign in url
    path('signinUser/', views.signInUser, name='signin_user'),

    # Sign out url
    path('signout/',views.signOut, name='signout'),

    # Upper Navigation Inherit Url
    path('upperNav/', views.UpperNav, name='upper-nav'),

    # Profile 
    path('profile/', views.Profile, name='profile'),
    path('profile/<user>/', views.OneUser, name='one_user'),
    path('updateProfile/', views.UpdateProfile, name='update_profile'),
    path('deleteUser/', views.DeleteUser, name='delete_user'),

    # Create new book
    path('NewBook/', views.NewBook, name='new_book'),
    path('getAllCategories/', views.getAllCategories, name='get_all_categories'),
    path('getCategoryInfo/', views.getCategoryInfo, name='get_category_info'),
    path('uploadBook/', views.UploadBook, name='upload_book'),
    path('deleteBook/', views.DeleteBook, name='delete_book'),
    path('borrowBook/', views.BorrowBook, name='borrow_book'),

    # Create new category
    path('NewCategory/', views.NewCategory, name='new_category'),
    path('createNewCategory/', views.CreateNewCategory, name='createNewCategory'),

    # All books
    path('AllBooks/', views.AllBooks, name='all_books'),
    path('getAllBooks/', views.getAllBooks, name='get_all_books'),
    path('book/<int:pk>', views.OneBook, name='one_book'),

    # ALl users
    path('AllUsers/', views.AllUsers, name='all_users'),
    path('getAllUsers/', views.getAllUsers, name='get_all_users'),

    # Transactions
    path('LibTransactions/', views.LibTransact, name='lib_transactions'),
    path('getLibTransactions/', views.getLibTransactions, name='get_lib_transactions'),
    path('MyTransactions/', views.MembTransact, name='member_transactions'),
    path('getMyTransactions/', views.getMyTransactions, name='get_my_transactions'),

]