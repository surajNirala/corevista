from . import views
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', views.home, name='home'),
    path('blog-category/', views.blog_category, name='blog_category'),
    path('blog-category1/', views.blog_category1, name='blog_category1'),
    path('blog-details', views.blog_details, name='blog_details'),
    path('blog/<int:id>/', views.single_blog_details, name='single_blog_details'),  # URL based on id
    path('blog/<slug:slug>/', views.blog_details_slug, name='blog_details_slug'),  # URL based on slug
    path('blog-create', views.blog_create, name='blog_create'),

]
