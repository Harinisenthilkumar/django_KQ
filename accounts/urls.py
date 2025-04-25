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
    path('addusers/', views.add_user_view, name='add_user'),
    path('edituser/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('deleteuser/<int:user_id>/', views.delete_user_view, name='delete_user'),
]