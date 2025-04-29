from django.urls import path
# # from . import views


# # urlpatterns = [
# #     path('login/', views.login_view, name='login'),
# #     path('dashboard/', views.dashboard_view, name='dashboard'),
# # ]
# from django.urls import path
# from . import views

# urlpatterns = [
#     # UI Views
#     path('login/', views.login_view, name='login'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('addusers/', views.add_user_view, name='add_user'),
#     path('edituser/<int:user_id>/', views.edit_user_view, name='edit_user'),
#     path('api/users/<int:user_id>/', views.user_delete, name='user-delete'),
#     # API Views
#     path('api/users/', views.user_list_create, name='user_list_create'),
#     path('api/users/<int:user_id>/', views.user_detail_view, name='user_detail_api'),  
    
# ]
# from django.urls import path
# from . import views

# urlpatterns = [
#     # UI Views
#     path('login/', views.login_view, name='login'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('addusers/', views.add_user_view, name='add_user'),
#     path('edituser/<int:user_id>/', views.edit_user_view, name='edit_user'),

#     # API Views
#     path('api/users/', views.user_list_create, name='user_list_create'),  # List & Create
#     path('api/users/<int:user_id>/', views.user_detail_view, name='user_detail_api'),  # Retrieve & Update
#     path('api/users/delete/<int:user_id>/', views.user_delete, name='user_delete_api'),  # DELETE separately
# ]
from . import views


urlpatterns = [
    #Template URL
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('dashboard/home/', views.dashboard_home_view, name='dashboard_home'),  
    path('addusers/', views.add_user_view, name='add_user'),
    path('edituser/<int:user_id>/', views.edit_user_page, name='edit_user_page'),   
    
    
    
    #API URL
    path('get_user_list', views.get_user_list, name='get_user_list'),
    path('create_user', views.create_user, name='create_user'), # API create 
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'), # API update
    path('api/usersDelete/<int:user_id>/', views.user_delete, name='user_delete'),   # API delete
    
    
    
    
   
    # Logout
    path('logout/', views.logout_view, name='logout'),
]

