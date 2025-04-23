# from django.urls import path
# from . import views


# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_user/', views.add_user_view, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    
  
]