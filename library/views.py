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
    return redirect('signin')

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

# One User
def OneUser(request,user):

    # Get the user using username
    user = User.objects.get(username = user)
    profile = models.Profile.objects.get(user = user)
    context = {'profile':profile}

    return render(request,'librarian/user.html',context)

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


# Delete User
def DeleteUser(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        username = request.POST.get('username')
        user = User.objects.get(username = username)
        
        # check if the user exists
        if not user:
            return JsonResponse({'status':'not_found'})
        else:
            user.delete()
            return JsonResponse({'status':'deleted'})


# Create new book
def NewBook(request):
    return render(request,'librarian/new_book.html')

# Get all categories
def getAllCategories(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Get all categories
        categories = models.Category.objects.all()

        # Check if there are no categories
        if not categories:
            return JsonResponse({'status':'empty'})
        
        else:
            # Create a list of categories
            category_list = []
    
            for category in categories:
                category_list.append(category.category_name)
    
            return JsonResponse({'status':'present','categories':category_list})
        
# Get category info
def getCategoryInfo(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Get the category name
        category_name = request.POST.get('category_name')

        # Get the category info
        category = models.Category.objects.get(category_name = category_name)
        # Get the category description
        category_description = category.category_description

        return JsonResponse({'category_description':category_description})
    
# Upload book
def UploadBook(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Get the data
        book_title = request.POST.get('book_title')
        book_author = request.POST.get('book_author')
        book_category = request.POST.get('selected_category')
        book_description = request.POST.get('book_desc')
        book_copies = request.POST.get('book_copies')
        book_pages = request.POST.get('book_pages')
        book_cover = request.FILES.get('cover_image')

        # Check if the book exists
        if models.Book.objects.filter(book_name = book_title).exists():
            return JsonResponse({'status':'exists'})
        else:
            # Create the book
            new_book = models.Book()
            new_book.book_name = book_title
            new_book.book_author = book_author
            # Get the category
            category = models.Category.objects.get(category_name = book_category)
            new_book.book_category = category
            #
            new_book.book_description = book_description
            new_book.all_copies = book_copies
            new_book.book_pages = book_pages
            new_book.book_cover = book_cover
            new_book.save()

            return JsonResponse({'status':'created'})

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
        
# All Books
def AllBooks(request):
    return render(request,'Main/all_books.html')

# Get all books
def getAllBooks(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Get category name
        category_name = request.POST.get('category')

        if(category_name == 'all'):
            # Get all books
            books = models.Book.objects.all()

        else:
            # Get the category
            category = models.Category.objects.get(category_name = category_name)
            # Get all books in the category
            books = models.Book.objects.filter(book_category = category)

        # Check if there are no books
        if not books:
            return JsonResponse({'status':'empty'})
        
        else:
            # Create a list of books
            book_list = []
    
            for book in books:

                available_copies = book.all_copies - book.given_copies

                one_book = {
                    'book_id':book.book_id,
                    'book_name':book.book_name,
                    'book_author':book.book_author,
                    'book_category':book.book_category.category_name,
                    'book_cover':book.book_cover.url,
                    'all_copies':book.all_copies,
                    'available_copies':available_copies,
                    'added_on':book.created.strftime('%d %b, %Y'),
                }

                book_list.append(one_book)
    
            return JsonResponse({'status':'present','books':book_list})

# One Book
def OneBook(request, pk):

    # Get the book
    book = models.Book.objects.get(book_id = pk)

    # check if the book exists
    if not book:
        # redirect to all books
        return redirect('all_books')
    else:
        available_copies = book.all_copies - book.given_copies
        context = {'book':book,'available_copies':available_copies}

        return render(request,'Main/book.html',context)

# delete book
def DeleteBook(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # Get the book id
        book_id = request.POST.get('book_id')
        # Get the book
        book = models.Book.objects.get(book_id = book_id)

        # Check if the book exists
        if not book:
            return JsonResponse({'status':'not_found'})
        else:
            book.delete()
            return JsonResponse({'status':'deleted'})

# All Users
def AllUsers(request):
    return render(request,'Librarian/all_users.html')