# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

        

#     return render(request, 'accounts/login.html')


# def dashboard_view(request):
#     if not request.user.is_authenticated:  
#         return redirect('login') 
    
    
#     return render(request, 'accounts/dashboard.html')

# from django.shortcuts import render, redirect, HttpResponse

# def login_view(request):
#     if request.method == 'POST':
       
#         return redirect('dashboard') 

#     return render(request, 'accounts/login.html')


# def dashboard_view(request):
#     return render(request, 'accounts/dashboard.html')

# def add_user_view(request):
#     return render(request, 'accounts/addusers.html')  

from django.shortcuts import render, redirect, HttpResponse
from .models import User 
def login_view(request):
    if request.method == 'POST':
        
        return redirect('dashboard')

    return render(request, 'accounts/login.html')


def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


def add_user_view(request):
    if request.method == 'POST':
        user_role = request.POST.get('userrole')
        user_name = request.POST.get('username')
        employee_id = request.POST.get('employee-id')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        email_id = request.POST.get('email')
        mobile_number = request.POST.get('mobile-number')
        is_active = request.POST.get('is-active') == 'yes'
        remarks = request.POST.get('remarks')
        is_locked = request.POST.get('is-locked') == 'yes'

        print(f"Received data: {request.POST}") 

        try:
            user = User(
                userRole=user_role,
                userName=user_name,
                employeeId=employee_id,
                department=department,
                designation=designation,
                emailId=email_id,
                mobileNumber=mobile_number,
                isActive=is_active,
                remarks=remarks,
                isAccountLocked=is_locked
            )
            user.save()
            print(f"User saved: {user.userName}") 
            return redirect('dashboard')
        except Exception as e:
            print(f"Error saving user: {e}")
            return HttpResponse(f"Error saving user: {e}")

    return render(request, 'accounts/addusers.html')