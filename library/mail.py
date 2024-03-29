# Handling all the Mails Here
from CatalogPoint import settings
from django.template.loader import get_template
# Send one mail
from django.core.mail import EmailMessage,get_connection
from . import models  

# Create a class for mailing 
class Mailer:

    # Initialise the class
    def __init__(self,subject,template_path):
        self.subject = subject
        self.template_path = template_path
        #self.from_email = settings.EMAIL_HOST_USER
        self.from_email = f'CodePinion Developers <{settings.EMAIL_HOST_USER}>'
        self.connection = get_connection(fail_silently=False)

    # Create email instance
    def Create_Email_Instance(self,subject,html_template,to_email):

        # Create Email Messages
        msg = EmailMessage(
            subject, 
            html_template, 
            self.from_email, 
            [to_email],
            connection=self.connection,
        )
        msg.content_subtype = "html"  # Main content is now text/html
        return msg
    
    # Method to send mail to a user
    def Send_Mail_To_User(self,data_dict,to_email):
        # Create and open a connection SMLP
        self.connection.open()

        # Create the template
        template = get_template(self.template_path)
        template_data = template.render(data_dict)

        # Create Email Messages
        msg = self.Create_Email_Instance(self.subject,template_data,to_email)
        msg.send()

        # Close the connection
        self.connection.close()

    # Method to send mail to all users
    def Send_Mail_To_All(self):

        # Get all the users
        all_profiles = models.Profile.objects.all()

        # Create email and username list
        email_list = []
        username_list = []

        # Loop through all the profiles
        for profile in all_profiles:

            # Append the email and username to the list
            email_list.append(profile.user.email)
            username_list.append(profile.full_name)

        # Send mail to all the users
        for user_email, user_username in zip(email_list, username_list):

            username_dict = {'username':user_username}
            email = user_email
            # Call the Send_Mail_To_User method
            self.Send_Mail_To_User(data_dict=username_dict,to_email=email)