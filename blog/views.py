from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from .models import BlogCategory,Blog
from blog.forms import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    data = {}
    data['title'] = "Blog List"
    # data['blogs'] = Blog.objects.using('blog_db').all()
    # data['MEDIA_URL']= settings.MEDIA_URL
    return render(request, 'blog/home.html',data) 

def blog_category(request):
    data = {}
    data['title'] = "Blog Category"
    return render(request, 'blog/blog-category.html', data)


def blog_details(request):
    data = {}
    data['title'] = "Blog Details"
    return render(request, 'blog/blog-details.html', data)


@login_required
def blog_category1(request):
    data = {}
    data['title'] = "Blog Category"
    data['blogs'] = Blog.objects.all()
    return render(request, 'blog/blog-category1.html', data)

def single_blog_details(request,id):
    data = {}
    data['title'] = "Blog Details"
    data['blog'] = get_object_or_404(Blog, id=id)
    return render(request, 'blog/blog-details1.html', data)

def blog_details_slug(request,slug):
    data = {}
    data['title'] = "Blog Details"
    data['blog'] = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog/blog-details1.html', data)

@login_required
def blog_create(request):
    data = {}
    current_path = request.path    
    # Optionally split URL into components (path, query, etc.)
    split_path = current_path.strip('/').split('/')
    data['current_url'] = current_path
    data['breadcrumb_parts'] = split_path
    data['title'] = "Blog Create"
    data['blog_categories'] = BlogCategory.objects.all()
    if request.method == 'POST': 
        form = forms.BlogForm(request.POST, request.FILES)  # Include FILES for image upload
        if form.is_valid():
            blog = form.save(commit=False)  # Don't save yet, we want to modify the instance
            blog.user = request.user  # Set the current logged-in user
            blog.save()
            messages.success(request, "Blog created successfully!")
            return redirect('blog_category1')  # Redirect to the blog list or another page after successful submission
        else:
            messages.error(request, "There were errors in your form. Please correct them.")
            data['form'] = form
    else: 
        form = forms.BlogForm()
        data['form'] = form
    return render(request, 'blog/blog-create.html', data)
    
    
