# from django.urls import path
# from . import views


# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    # UI Views
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('addusers/', views.add_user_view, name='add_user'),
    path('edituser/<int:user_id>/', views.edit_user_view, name='edit_user_page'), 
    path('api/users/<int:user_id>/', views.user_delete, name='user-delete'),
    # API Views
    path('api/users/', views.user_list_create, name='user_list_create'),
    path('api/users/<int:pk>/', views.user_detail_view, name='user_detail_api'),  
]
