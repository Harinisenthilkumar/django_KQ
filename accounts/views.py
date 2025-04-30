from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, LoginCredentials
from .serializers import UserSerializer
from django.http import JsonResponse
import datetime
from functools import wraps
import jwt
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, LoginCredentials
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt


def jwt_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')

        if not token:
            return redirect('/accounts/login/')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload.get('id')
        except jwt.ExpiredSignatureError:
            return redirect('/accounts/login/')
        except jwt.DecodeError:
            return redirect('/accounts/login/')
        print(token)
        return view_func(request, *args, **kwargs)
    return wrapped_view


#Template Views
@jwt_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')\
        
@jwt_required
def add_user_view(request):
    return render(request, 'accounts/addusers.html')

@jwt_required
def edit_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'accounts/edituser.html', {'user': user})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            credentials = LoginCredentials.objects.get(email=email, password=password)
            user = User.objects.get(emailId=email)

            # simple JWT payload without expiry
            payload = {
                'id': user.id,
                'emailId': user.emailId,
                'iat': datetime.datetime.utcnow()
               
            }
            SECRET_KEY = 'django-insecure-*n-0cm1bk_3ti(f^agvd&gkv6upaweac)2l=#!f4c7eqqyo5b8'
            
            # Encode the token
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
          
            # Set the cookie without expiry
            response = redirect('dashboard')
            response.set_cookie(
                key='jwt',
                value=token,
                httponly=True
                # No max_age or expires → cookie becomes a "session cookie"
            )

            return response

        except (LoginCredentials.DoesNotExist, User.DoesNotExist):
            messages.error(request, 'Invalid credentials.')

    return render(request, 'accounts/login.html')
    
@jwt_required    
@api_view(['GET'])
def get_user_list(request):
    users = User.objects.filter(is_deleted=False)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)



@csrf_exempt
@jwt_required
@api_view(['POST'])
def create_user(request):
    try:
        data = request.data.copy()
        print("Incoming Data =====>")
        print(data)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            LoginCredentials.objects.create(
                user=user,
                email=user.emailId,
                password=data.get('password') or 'Default@123'
            )

            print("User Created Successfully!")
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors =====>")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception occurred =====>")
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@jwt_required  
@csrf_exempt      
@api_view(['PUT'])
def user_edit(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User updated successfully!'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@jwt_required  
@api_view(['DELETE'])
def user_delete(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_deleted = True
    user.save()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)










@jwt_required  
def edit_user_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/edituser.html', {'user': user})







@jwt_required  
def dashboard(request):
    token = request.COOKIES.get('jwt')  
    if not token:
        return redirect('/accounts/login/')
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return redirect('/accounts/login/')
    return render(request, 'accounts/dashboard.html')


@jwt_required
def dashboard_home_view(request):
    return render(request, 'accounts/dashboardhome.html')




@csrf_exempt
def logout_view(request):
    response = redirect('login') 
    response.delete_cookie('jwt') 
    return response