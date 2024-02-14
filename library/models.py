from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# User Profile
class Profile(models.Model):

    # One profile owned by one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The Profile class attributes
    profile_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50, verbose_name='Full Name')

    bio = models.TextField(verbose_name='Bio')
    company = models.CharField(max_length=20, verbose_name='Company')
    location = models.TextField(verbose_name='Location')
    secondary_email = models.URLField(max_length = 200, verbose_name='Secondary Email', default='Secondary Email')
    website = models.URLField(max_length = 200, verbose_name='Website')

    profile_pic = models.ImageField(upload_to = 'Profiles', verbose_name='Profile Picture')

    update = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    @property
    def profile_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url 
        

# Book category
class Category(models.Model):

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20, verbose_name='Category Name')
    category_description = models.TextField(verbose_name='Category Description')

    # These users appreciate this category
    followers = models.ManyToManyField(Profile, related_name='followers', verbose_name='Followers')

    update = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name
    
# Book
class Book(models.Model):

    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=50, verbose_name='Book Name')
    book_author = models.CharField(max_length=50, verbose_name='Book Author')
    book_description = models.TextField(verbose_name='Book Description')
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Book Category')
    book_cover = models.ImageField(upload_to = 'Books', verbose_name='Book Cover')
    book_pages = models.IntegerField(verbose_name='Book Pages', default=0)

    all_copies = models.IntegerField(verbose_name='All Copies', default=0)
    given_copies = models.IntegerField(verbose_name='Given Copies',default=0)
    users_who_have = models.ManyToManyField(Profile, related_name='users_who_have', verbose_name='Users Who Have')

    update = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book_name

    @property
    def book_url(self):
        if self.book_cover and hasattr(self.book_cover, 'url'):
            return self.book_cover.url