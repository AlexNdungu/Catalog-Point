from django.contrib.auth.models import User
from .resorce import Create_User_Signal
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
#
from .mail import Mailer
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_save,post_save
from django.contrib.sites.models import Site


# Create an class adapter that customises user registration
class RegisterAdapter(DefaultSocialAccountAdapter):

    # Override the save_user method
    def save_user(self, request, sociallogin, form=None):

        # Check the process is signup or signin
        if sociallogin.state.get('process') == 'signup' or sociallogin.state.get('process') == 'signin':

            # Check if user already exists
            if User.objects.filter(email=sociallogin.user.email).exists():

                # Get the user from the social login
                user = User.objects.get(email=sociallogin.user.email)

                # Check if user is authenticated using 0auth
                if user.socialaccount_set.filter(provider=sociallogin.account.provider).exists():

                    # Call the super method to execute the default save_user logic
                    super().save_user(request, sociallogin, form)

                    # Return the user
                    return user

                else:

                    # Add the social account to the user
                    sociallogin.connect(request, user)

                    # Call the super method to execute the default save_user logic
                    super().save_user(request, sociallogin, form)

                    # Return the user
                    return user
            
            else:

                # Get the user from the social login
                user = sociallogin.user

                # Set username to email
                user.username = user.email

                # Save the user
                user.save()

                # Call the super method to execute the default save_user logic
                super().save_user(request, sociallogin, form)

                #Return the user
                return user


# Function that send email to users when they are created
@receiver(post_save, sender=User)
def Welcome_User_Signal(sender,instance,created, **kwargs):

    if created:

        # Call the create user function
        new_user = Create_User_Signal(user=instance)

        # check if user has email
        if new_user.email != '':
            
            # Instanciate the Mailer class
            subject = 'Welcome to CatalogPoint'
            template_path = 'Mail/welcome.html'
            mailer = Mailer(subject,template_path)
            # Get the instance username and email
            username_dict = {'username':new_user.username}
            email = new_user.email
            # Call the Send_Mail_To_User method
            mailer.Send_Mail_To_User(data_dict=username_dict,to_email=email)
