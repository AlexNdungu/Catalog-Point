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

    # Profile Url
    path('profile/', views.Profile, name='profile'),

    # Update Profile Url
    path('updateProfile/', views.UpdateProfile, name='update_profile'),

    # Create new book
    path('NewBook/', views.NewBook, name='new_book'),
    path('getAllCategories/', views.getAllCategories, name='get_all_categories'),
    path('getCategoryInfo/', views.getCategoryInfo, name='get_category_info'),

    # Create new category
    path('NewCategory/', views.NewCategory, name='new_category'),
    path('createNewCategory/', views.CreateNewCategory, name='createNewCategory'),

]