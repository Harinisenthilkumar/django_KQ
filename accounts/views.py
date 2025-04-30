from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from .models import User
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer




from accounts.models import User, LoginCredentials


DEFAULT_ADMIN_EMAIL = 'admin01@gmail.com'
DEFAULT_ADMIN_PASSWORD = 'Admin@01'


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if credentials exist
            credentials = LoginCredentials.objects.get(email=email, password=password)

            # Get the associated User object
            user = User.objects.get(emailId=email)

            # Attach user ID in session manually
            request.session['user_id'] = user.id
            request.session['user_name'] = user.userName


            messages.success(request, f"Welcome, {user.userName}!")
            return redirect('dashboard')

        except LoginCredentials.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'User not found for the given email.')

    return render(request, 'accounts/login.html')




def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


def add_user_view(request):
    return render(request, 'accounts/addusers.html')





@api_view(['GET', 'POST',]) 
def user_list_create(request, user_id=None):
    if request.method == 'GET':
        users = User.objects.filter(is_deleted=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
              
# @api_view(['DELETE'])
# def user_delete(request, user_id):
#     try:
#         user = User.objects.get(pk=user_id)
#         user.is_deleted = True
#         user.save()
#         return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 

@api_view(['DELETE'])
def user_delete(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    
    
        
@api_view(['GET', 'POST'])
def edit_user_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retrieve the current user data
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
     
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def user_detail_view(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)