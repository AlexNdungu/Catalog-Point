from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from . import models


# Sign up page
def signUp(request):

    # Check if user is authenticated
    if request.user.is_authenticated:
        return redirect('upper-nav')
    else:
        return render(request,'Main/signup.html', {'error':''})

# Create new user
def createNewUser(request):

    #Email will always be unique for any user

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Now we check if the user exists
        if User.objects.filter(email=email).exists():
            
            return JsonResponse({'status':'exists'})

        else:

            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password)

            # Check if the user is logged in
            if not request.user.is_authenticated:
                # Login the user
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')

            # Redirect the user to the dash page
            return JsonResponse({'status':'created'})
        
# Sign in page
def signIn(request):

    # Check if user is authenticated
    if request.user.is_authenticated:
        return redirect('dash')
    else:
        return render(request,'Main/signin.html',{'error':''})

# Sign out user
def signOut(request):  
    logout(request)
    return redirect('landing')

# Sign in user
def signInUser(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists
        if User.objects.filter(email=email).exists():

            # Get the user
            user = User.objects.get(email=email)

            # Check if the password is correct
            if user.check_password(password):

                # Login the user
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')

                # Redirect the user to the dash page
                return JsonResponse({'status':'found'})

            else:

                return JsonResponse({'status':'wrong_password'})

        else:

            return JsonResponse({'status':'not_found'})

# The Inherited upper Navigation Rendering Function
def UpperNav(request):
    return render(request,'Inherit/upper-nav.html')

# The profile rendering function
@login_required
def Profile(request):

    # Get the profile picture url of current user
    profile = models.Profile.objects.get(user = request.user)

    if profile.profile_pic != '':
        profile_pic_url = profile.profile_pic.url
    else:
        profile_pic_url = ''

    data_dict = {
        'profile_pic_url':profile_pic_url,
    }

    return render(request, 'Main/profile.html', data_dict)

# Update Profile
def UpdateProfile(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Get the data
        update_item = request.POST.get('to_update')
        # Get the current profile
        current_profile = models.Profile.objects.get(user = request.user)

        # Updating profile picture
        if update_item == 'profile_pic':
                
            # Get the profile picture
            profile_pic = request.FILES.get('profile_pic')
            # Update the profile picture
            current_profile.profile_pic = profile_pic
            current_profile.save()
            profile_pic_url = current_profile.profile_pic.url

            return JsonResponse({'profile_pic_url':profile_pic_url})
        
        elif update_item == 'remove_profile_pic':

            # Delete the profile picture
            default_storage.delete(current_profile.profile_pic.path)
            current_profile.profile_pic = None
            current_profile.save()

            return JsonResponse({'message':'suceess'})
        
        elif update_item == 'bio':

            # Get the bio
            bio = request.POST.get('bio')
            current_profile.bio = bio
            current_profile.save()
            # Get the new bio
            bio = current_profile.bio

            return JsonResponse({'bio':bio})
        
        elif update_item == 'all_details':

            # Get the data : fullname,secondary_email,company,location,website
            full_name = request.POST.get('fullname')
            secondary_email = request.POST.get('secondary_email')
            company = request.POST.get('company')
            location = request.POST.get('location').capitalize()
            website = request.POST.get('website')

            # Update the data
            current_profile.full_name = full_name
            current_profile.secondary_email = secondary_email
            current_profile.company = company
            current_profile.location = location
            current_profile.website = website
            current_profile.save()

            # Get the new data
            new_full_name = current_profile.full_name
            new_secondary_email = current_profile.secondary_email
            new_company = current_profile.company
            new_location = current_profile.location
            new_website = current_profile.website

            return JsonResponse({'fullname':new_full_name,'secondary_email':new_secondary_email,'company':new_company,'location':new_location,'website':new_website})

# Create new book
def NewBook(request):
    return render(request,'librarian/new_book.html')

# Create new category
def NewCategory(request):
    return render(request,'librarian/new_category.html')

# Create new category functionality
def CreateNewCategory(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Get the category name and description
        category_title = request.POST.get('categ_title').title()
        category_description = request.POST.get('categ_description')

        # Check if the category exists
        if models.Category.objects.filter(category_name = category_title).exists():
            return JsonResponse({'status':'exists'})
        else:
            # Create the category
            new_category = models.Category()
            new_category.category_name = category_title
            new_category.category_description = category_description
            new_category.save()

            return JsonResponse({'status':'created'})