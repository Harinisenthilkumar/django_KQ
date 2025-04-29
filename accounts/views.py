
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, LoginCredentials
from .serializers import UserSerializer
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model


# from django.contrib.auth.models import User

#Template Views
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def add_user_view(request):
    return render(request, 'accounts/addusers.html')

def edit_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'accounts/edituser.html', {'user': user})



#API Views
User = get_user_model()

# DEFAULT_ADMIN_EMAIL = 'admin01@gmail.com'
# DEFAULT_ADMIN_PASSWORD = 'Admin@01'
#Login Create API
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            credentials = LoginCredentials.objects.get(email=email, password=password)
            user = User.objects.get(emailId=email)

            request.session['user_id'] = user.id
            request.session['user_name'] = user.username

            messages.success(request, f"Welcome, {user.username}!")
            return redirect('dashboard')

        except LoginCredentials.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'User not found for the given email.')

    return render(request, 'accounts/login.html')
    
    
#List Grid User API 
@api_view(['GET'])
def get_user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
    
#Create User    
@api_view(['POST'])
def create_user(request):
    data = request.data.copy()

    # ✅ Ensure 'username' exists for AbstractUser
    if 'username' not in data or not data['username']:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()

        # ✅ Save LoginCredentials also
        LoginCredentials.objects.create(
            user=user,
            email=user.emailId,
            password=data.get('password') or 'Default@123'
        )

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['PUT'])
def user_edit(request, user_id):
    print("hitted@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    try:
        user = User.objects.get(pk=user_id)
        print(user,"!!!!!!!!!!!!!!!!!!!!")
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Handle partial updates (update only the fields provided)
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User updated successfully!'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT'])
# def user_detail_view(request, user_id):
#     try:
#         user = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'User updated successfully!'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def user_delete(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


def edit_user_page(request, user_id):
  
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/edituser.html', {'user': user})











def dashboard(request):
    token = request.COOKIES.get('jwt')  
    if not token:
        return redirect('/accounts/login/')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return redirect('/accounts/login/')
    except jwt.DecodeError:
        return redirect('/accounts/login/')

    return render(request, 'accounts/dashboard.html')

# views.py
def dashboard(request):
    token = request.COOKIES.get('jwt')  
    if not token:
        return redirect('/accounts/login/')
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return redirect('/accounts/login/')
    return render(request, 'accounts/dashboard.html')
