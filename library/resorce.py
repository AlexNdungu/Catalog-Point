from . import models
from django.contrib.auth.models import User
from .generate import UserGen


# Create User Signal
def Create_User_Signal(user):

    #Create a profile for the user
    profile = models.Profile(user=user)
    #Save the profile
    profile.save()

    suggest_username = ''
    stripped_mail = ''

    # Check if user has email
    if user.email == '':

        stripped_mail = user.username
    
    else:
        #Get the instance of user created 
        new_user_email = user.email
        #Strip the email
        stripped_mail = new_user_email.split('@')[0]

    #Check if the an email exists matching stripped mail
    if User.objects.filter(username=stripped_mail).exists():

        #Get the newly craeted profile id
        profile_id = str(profile.profile_id)
        #Create a new username with stripped mail and profile id
        new_username = stripped_mail + profile_id

        if User.objects.filter(username=new_username).exists():

            #count the numebr of profiles 
            profile_count = models.Profile.objects.count()
            #
            profile_count = profile_count + 1000
            #Get a list of existing usernames
            usernames = User.objects.values_list("username")
            # Convert the QuerySet to a list
            usernames = list(usernames)

            #initialise the UserName Generator Class
            username_gen = UserGen(new_user_email,profile_count)
            #Call the GenMoreName method
            generated_username = username_gen.GenMoreName(1,usernames)[0]

            #Assign the suggested_username to generated_username
            suggest_username = generated_username

        else:

            #Assign the suggested name to new_username
            suggest_username = new_username

    else:

        #Assign the suggested name to stripped_mail
        suggest_username = stripped_mail  

    #Change username from email to suggest_username
    user.username = suggest_username
    #Now give this profile a full name
    profile.full_name = suggest_username

    # Save the changes to the database
    profile.save()
    user.save()

    return user