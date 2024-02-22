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


# Cost
class Cost(models.Model):

    cost_id = models.AutoField(primary_key=True)
    cost_name = models.CharField(max_length=50, verbose_name='Cost Name')
    cost_description = models.TextField(verbose_name='Cost Description')
    cost_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cost Amount')

    update = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cost_name
    
# Book transaction
class Transaction(models.Model):

    transaction_id = models.AutoField(primary_key=True)
    transaction_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Transaction Profile')
    transaction_book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Transaction Book')
    transaction_cost = models.IntegerField(verbose_name='Transaction Cost', default=0)

    transaction_from_date = models.DateField(verbose_name='Transaction From Date')
    transaction_to_date = models.DateField(verbose_name='Transaction To Date')
    transaction_no_of_days = models.IntegerField(verbose_name='Transaction No Of Days', default=0)

    transaction_approved = models.BooleanField(verbose_name='Transaction Approved', default=False)
    transaction_denied = models.BooleanField(verbose_name='Transaction Denied', default=False)
    transaction_returned = models.BooleanField(verbose_name='Transaction Returned', default=False)

    update = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.transaction_profile.full_name + ' - ' + self.transaction_book.book_name + ' - ' + str(self.transaction_id)
