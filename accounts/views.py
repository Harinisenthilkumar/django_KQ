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

from django.shortcuts import render, redirect, HttpResponse, redirect, get_object_or_404, HttpResponse
from .models import User 
def login_view(request):
    if request.method == 'POST':
        
        return redirect('dashboard')

    return render(request, 'accounts/login.html')


def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import User

def dashboard_view(request):
    users = User.objects.all().values(
        'id',
        'userRole',
        'userName',
        'emailId',
        'department',
        'designation',
        'mobileNumber',
        'isActive'
    )
    user_data_for_grid = []
    for user in users:
        user_data_for_grid.append({
            'id': user['id'],
            'actions': '',
            'userRole': user['userRole'],
            'userName': user['userName'],
            'emailId': user['emailId'],
            'department': user['department'],
            'designation': user['designation'],
            'mobileNumber': user['mobileNumber'],
            'status': 'Active' if user['isActive'] else 'Inactive',
        })

    context = {
        'rowData': user_data_for_grid,
    }
    return render(request, 'accounts/dashboard.html', context)
def add_user_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')  # Use the correct form field name
        email_id = request.POST.get('email')      # Use the correct form field name
        user_role = request.POST.get('userrole')  # Use the correct form field name
        department = request.POST.get('department') # Use the correct form field name
        designation = request.POST.get('designation') # Use the correct form field name
        mobile_number = request.POST.get('mobile-number') # Use the correct form field name
        is_active_str = request.POST.get('is-active')
        is_active = True if is_active_str == 'yes' else False
        remarks = request.POST.get('remarks')
        is_account_locked_str = request.POST.get('is-locked')
        is_account_locked = True if is_account_locked_str == 'yes' else False

        # Basic validation
        if not user_name or not email_id or not user_role:
            return render(request, 'accounts/addusers.html', {'error': 'Please fill in all required fields.'})

        User.objects.create(
            userName=user_name,
            emailId=email_id,
            userRole=user_role,
            department=department,
            designation=designation,
            mobileNumber=mobile_number,
            isActive=is_active, 
            remarks=remarks,
            isAccountLocked=is_account_locked, 
        )
        return redirect('dashboard')
    return render(request, 'accounts/addusers.html')

def edit_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.userRole = request.POST.get('userrole')
        user.userName = request.POST.get('username')
        user.department = request.POST.get('department')
        user.designation = request.POST.get('designation')
        user.emailId = request.POST.get('email')
        user.mobileNumber = request.POST.get('mobile-number')
        user.isActive = request.POST.get('is-active') == 'yes'
        user.remarks = request.POST.get('remarks')
        # user.isAccountLocked = request.POST.get('is-locked') == 'yes'
        user.save()
        return redirect('dashboard')
    else:
        context = {
            'user': user,
        }
        return render(request, 'accounts/edituser.html', context)

def delete_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('dashboard')  
