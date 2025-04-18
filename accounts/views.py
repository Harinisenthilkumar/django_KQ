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

from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        # No need to check username or password
        return redirect('dashboard') 

    return render(request, 'accounts/login.html')


def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')
