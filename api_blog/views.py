from blog.models import Blog
from django.http import JsonResponse
from django.db import connection
import re

def blogList(request):
    field_names = [field.name for field in Blog._meta.fields]
    print(field_names)
    # blogs = Blog.objects.all().values('id', 'category','category_id','title', 'slug', 'summary', 'description')
    # blogs = Blog.objects.all().values(*field_names)
    # blogs = Blog.objects.all().values()
    # data = list(blogs)  # Convert QuerySet to a list of dictionaries
    # blogs = Blog.objects.raw("select * from blogs b left join blog_categories bc on bc.id = b.category_id")
    query = """
            SELECT 
                blogs.id AS blog_id,
                blogs.title AS blog_title,
                blogs.slug AS blog_slug,
                blogs.summary,
                blogs.description,
                blogs.photo,
                blogs.status,
                blogs.created_at,
                blogs.updated_at,
                blog_categories.id AS category_id,
                blog_categories.name AS category_name
            FROM blogs
            LEFT JOIN blog_categories ON blog_categories.id = blogs.category_id
        """
        
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        data = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    # data = [
    #     {
    #         "blog_id": blog.id,
    #         "user": blog.user_id,
    #         "category": blog.category_id,
    #         "category_name": blog.name,
    #         "title": blog.title,
    #         "slug": blog.slug,
    #         "summary": blog.summary,
    #         "description": blog.description,
    #         "photo": blog.photo.url if blog.photo else None,
    #         "status": blog.status,
    #         "created_at": blog.created_at,
    #         "updated_at": blog.updated_at,
    #     }
    #     for blog in blogs
    # ]
    response = {
        "code": 200,
        "message": "Fetched User List",
        "data": data,
    }
    return JsonResponse(response, safe=False, json_dumps_params={'indent': 2})

def blogDetail(request, pk):
    if not re.match(r'^\d+$', pk):
        return JsonResponse({
            "code": 400,
            "message": "Invalid blog ID format",
            "data": None
        }, status=400)
    try:
        blog = Blog.objects.get(pk=pk)
        data = {
            "blog_id": blog.id,
            "user": blog.user_id,
            "category": blog.category_id,
            "title": blog.title,
            "slug": blog.slug,
            "summary": blog.summary,
            "description": blog.description,
            "photo": blog.photo.url if blog.photo else None,
            "status": blog.status,
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
        }  # Convert model instance to a dictionary
        response = {
            "code": 200,
            "message": "Fetched Blog Details",
            "data": data
        }
    except Blog.DoesNotExist:
        response = {
            "code": 404,
            "message": "Blog not found",
            "data": None
        }
    
    return JsonResponse(response, status=200,safe=False)
