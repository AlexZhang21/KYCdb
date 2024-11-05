from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loginPage, name='Login'),
    path('admin_user_details/', views.aduserPage, name='Ad_User_details'),
    path('create_new_user/', views.create_new_user, name='New_User_details'),
    path('user_details/<int:pk>/', views.userPage, name='User_details'),
    path('company_file/<int:pk>/', views.company_file, name='Company_file'),
    path('download_file/<int:pk>/', views.download_file, name='Download_File'),
    path('edit_company_details/<int:pk>/', views.edit_Company, name='Edit_Company'),
    path('change_password/<int:pk>/', views.changePassword, name='Change_Password'),
    path('delete_user/<str:username>/', views.del_user, name='Delete_User'),
    path('delete_comp_record/<int:pk>/', views.del_item, name='Delete_Company_Record'),
    path('delete_file/<int:pk>/', views.delete_file, name='Delete_File'),
    path('content_table/', views.homePage, name='Home'),
    path('create_company/', views.create_company_form, name='Company_Create'),
    path('company_details/<int:pk>', views.companyPage, name='Comp_details'),
    path('Logout/', views.logoutAction, name='Logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)