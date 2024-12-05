from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import re

import json

@csrf_exempt
def userList(request):

    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password1 = data.get('password1')
            password2 = data.get('password2')
            
            if password1 != password2:
                response = {
                    "code": 422,
                    "message": "Password do not match!",
                    "data": None
                }
                return JsonResponse(response, status=422,safe=False)  
                
            if User.objects.filter(username=username).exists():
                response = {
                    "code": 422,
                    "message": "User already taken!",
                    "data": None
                }
                return JsonResponse(response, status=422,safe=False) 
            
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            response = {
                "code": 201,
                "message": "User created successfully.",
                "data": {"username": user.username, "email": user.email}
            }
            return JsonResponse(response, status=201, safe=False)
        
        except json.JSONDecodeError:
            response = {
                "code": 400,
                "message": "Invalid JSON format.",
                "data": None
            }
            return JsonResponse(response, status=400, safe=False)

    # Get all field names from the User model
    field_names = [field.name for field in User._meta.fields]

    # Fetch all user records and convert them into a list of dictionaries
    users = User.objects.all().values(*field_names)  # Use field names dynamically
    data = list(users)  # Convert QuerySet to a list of dictionaries

    # Prepare the response
    response = {
        "code": 200,
        "message": "Fetched User List.",
        "data": data,
    }

    # Return the response as JSON
    return JsonResponse(response, safe=False, json_dumps_params={'indent': 2})


def userList1(request):

    # Get all field names from the User model
    field_names = [field.name for field in User._meta.fields]

    # Fetch all user records and convert them into a list of dictionaries
    users = User.objects.all().values(*field_names)  # Use field names dynamically
    data = list(users)  # Convert QuerySet to a list of dictionaries

    # Prepare the response
    response = {
        "code": 200,
        "message": "Fetched User List.",
        "data": data,
    }

    # Return the response as JSON
    return JsonResponse(response, safe=False, json_dumps_params={'indent': 2})


def userDetail(request, pk):
    if not re.match(r'^\d+$', pk):
        return JsonResponse({
            "code": 400,
            "message": "Invalid user ID format",
            "data": None
        }, status=400)
    try:
        user = User.objects.get(pk=pk)
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "date_joined": user.date_joined,
            # Add other fields as needed
        }
        response = {
            "code": 200,
            "message": "Fetched User Details",
            "data": user_data
        }
    except User.DoesNotExist:
        response = {
            "code": 404,
            "message": "User not found",
            "data": None
        }
    
    return JsonResponse(response, status=200,safe=False)
