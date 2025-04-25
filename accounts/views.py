from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from .models import User
from django.urls import reverse
from accounts.models import User, LoginCredentials


DEFAULT_ADMIN_EMAIL = 'admin01@gmail.com'
DEFAULT_ADMIN_PASSWORD = 'Admin@01'

# def login_view(request):
#     if request.method == 'POST':  
#         email = request.POST.get('username')
#         password = request.POST.get('password')
#         print(f"Login attempt - Email: '{email}', Password: '{password}'")

#         try:
#             credentials = LoginCredentials.objects.get(email=email, password=password)

#             user = User.objects.get(emailId=email) 
#             login(request, user)  # ✅ Corrected from login_view() to login()

#             print("Login successful, redirecting to dashboard")
#             return redirect('dashboard')
#         except LoginCredentials.DoesNotExist:
#             messages.error(request, 'Invalid login credentials.')
#         except User.DoesNotExist:
#             messages.error(request, "User account not found for these credentials.")

#     return render(request, 'accounts/login.html')


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
    # Fetch users who are not marked as deleted
    users = User.objects.filter(is_deleted=False).values(
        'id', 'userRole', 'userName', 'emailId', 'department',
        'designation', 'mobileNumber', 'isActive'
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

    context = {'rowData': user_data_for_grid}
    return render(request, 'accounts/dashboard.html', context)






def add_user_view(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        user_role = request.POST.get('userrole')
        user_name = request.POST.get('username')
        email_id = request.POST.get('email')
        department = request.POST.get('department')
        employee_id = request.POST.get('employeeId')
        designation = request.POST.get('designation')
        mobile_number = request.POST.get('mobile-number')
        is_active = request.POST.get('is-active') == 'yes'
        is_locked = request.POST.get('is-locked') == 'yes'
        account_locked_remarks = request.POST.get('accountLockedRemarks', '')  # Get the new field

        # Create a new User record
        new_user = User(
            userRole=user_role,
            userName=user_name,
            emailId=email_id,
            department=department,
            employeeId=employee_id,
            designation=designation,
            mobileNumber=mobile_number,
            isActive=is_active,
            isAccountLocked=is_locked,
            remarks=account_locked_remarks, # save remarks.
        )
        new_user.save()

        # Redirect to the dashboard after saving the user
        return redirect(reverse('dashboard'))  # Use reverse to get the URL

    return render(request, 'accounts/addusers.html')



def dashboard(request):
    # Your dashboard logic here.  For example, fetch users to display.
    users = User.objects.all()  # Get all users
    context = {'users': users}
    return render(request, 'accounts/dashboard.html', context)

def edit_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.userRole = request.POST.get('userrole')
        user.userName = request.POST.get('username')
        user.employeeId = request.POST.get('employeeid')
        user.department = request.POST.get('department')
        user.designation = request.POST.get('designation')
        user.emailId = request.POST.get('email')
        user.mobileNumber = request.POST.get('mobile-number')
        user.isActive = request.POST.get('is-active') == 'yes'
        user.remarks = request.POST.get('remarks')
        user.isAccountLocked = request.POST.get('is-locked') == 'yes'
        user.save()

        return redirect('dashboard')
    
    context = {'user': user}
    return render(request, 'accounts/edituser.html', context)

def delete_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_deleted = True
    user.save()
    return redirect('dashboard')
