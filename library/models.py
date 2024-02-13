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