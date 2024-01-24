import logging

from django.http import JsonResponse 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import messages
from django.contrib import auth

 
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect 
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth.hashers import check_password


logger = logging.getLogger(__name__)





# @api_view(['POST'])
# def login(request):    
#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']): 
#         return Response({'details': 'User Credentials are Incorrect'}, status=status.HTTP_404_NOT_FOUND)
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(instance=user)    
#     return Response({"token": token.key, "user": serializer.data})

def register_view(request): 
     return render(request, 'register.html')
 
 
# def register_action(request):
#     if request.method == 'POST': 
#         form = RegisterUserForm(request.POST)   
#         if form.is_valid():
#             form.save()
#             # first_name = form.cleaned_data['first_name'] 
#             # last_name  = form.cleaned_data['last_name'] 
#             # username  = form.cleaned_data['username'] 
#             # user = authenticate(request, username)
            
#             # if user is not None:
#         else:
#         # Display form errors
#             for field, errors in form.errors.items():
#                 for error in errors:                     
#                     messages.warning(request, f"{field.capitalize()}: {error}")   
                
#     return render(request, 'register.html') 
 
def register_action(request):
          
    form = RegisterUserForm(request.POST)   
     
    if request.method == 'POST':     
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1']) 
            user.is_active = True
            user.is_staff = True 
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login_view')  # Redirect to the login page after successful registration
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:                     
                    messages.warning(request, f"{field.capitalize()}: {error}")   
                    # messages.warning(request, f"{error}")   

    return render(request, 'register.html')
 
 
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)        
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Adjust authentication as needed
@permission_classes([IsAuthenticated])  # Require authentication to access this view
def view_profile(request):
    user_profile = request.user  # Assuming UserProfile is related to User
    serializer = UserProfileSerializer(user_profile)  # Use your UserProfile serializer
    return Response(serializer.data)

def login_view(request): 
    return render(request, 'login.html')
 
 
    

def login_action(request):
    try: 
        if request.user.is_authenticated:
            return redirect('/dashboard')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')  

            user_exist = User.objects.filter(username=username)
             
            
            if not user_exist.exists():
                messages.warning(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
          
            user_obj = authenticate(request, username=username, password=password)  
           
           
            logger.info(f"Login attempt for username: {username}")
            logger.info(f"Login attempt for password: {password}")
            logger.info(f"Login attempt for outer: {user_obj}")
            
            if  user_obj and user_obj is not None:   
                auth.login(request, user_obj)
                # return redirect(reverse('dashboard'),permanent=True) 
                return redirect('/dashboard') 
            else: 
                messages.warning(request, 'Invalid Password')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         

    except Exception as e:
        # Log the exception for debugging
        logger.error(f"An error occurred: {e}")
        print(e)  # This will print the exception to the console for immediate debugging

 


def dashboard(request): 
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html') 

def logout_view(request):
    logout(request)
    return redirect('login_view')

 
    
    
def profile_view(request):
    # Check if the user is authenticated
    # logger.info(f"profile_view {request.session.get('first_name')}") 
    
    
    if request.user.is_authenticated: 

        # Pass user details to the template
        context = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
            'last_login': request.user.last_login,
        }

        # Render the profile template with user details
        return render(request, 'profile.html', context)
    else:
        # Handle the case where the user is not authenticated
        return render(request, '404.html')
        
def user_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Retrieve all users from the auth_user table
        all_users = User.objects.all()

        # Pass the list of users to the template
        context = {
            'all_users': all_users,
        }

        # Render the template with the list of users
        return render(request, 'tables.html', context)
    else:
        # Handle the case where the user is not authenticated
        return render(request, '404.html')
    
 