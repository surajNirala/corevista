from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.urls import views as auth_views
from . import views

urlpatterns = [
    path('users/', views.userList, name='userList'),
    path('users1/', views.userList1, name='userList1'),
    path('users/<str:pk>/', views.userDetail, name='userDetail'),
] 
