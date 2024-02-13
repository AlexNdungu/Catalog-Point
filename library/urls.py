from django.urls import path
from . import views

urlpatterns = [
    # Sign up url
    path('signup/',views.signUp, name='sign_up'),

    # Create new user
    path('createNewUser/', views.createNewUser, name='create_new_user'),

    # Sign in url
    path('signin/',views.signIn, name='signin'),

    # Sign out url
    path('signout/',views.signOut, name='signout'),

    # Sign in url
    path('signinUser/', views.signInUser, name='signin_user'),

    # landing Page Url
    path('', views.Landing, name='landing'),

]