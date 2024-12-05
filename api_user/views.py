from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
import re

def userList(request):
    # Get all field names from the User model
    field_names = [field.name for field in User._meta.fields]

    # Fetch all user records and convert them into a list of dictionaries
    users = User.objects.all().values(*field_names)  # Use field names dynamically
    data = list(users)  # Convert QuerySet to a list of dictionaries

    # Prepare the response
    response = {
        "code": 200,
        "message": "Fetched User List",
        "data": data,
    }

    # Return the response as JSON
    return JsonResponse(response, safe=False, json_dumps_params={'indent': 2})


def userDetail(request, pk):
    if not re.match(r'^\d+$', pk):
        return JsonResponse({
            "code": 400,
            "message": "Invalid blog ID format",
            "data": None
        }, status=400)
    try:
        user = User.objects.get(pk=pk)
        response = {
            "code": 200,
            "message": "Fetched Blog Details",
            "data": user
        }
    except User.DoesNotExist:
        response = {
            "code": 404,
            "message": "Blog not found",
            "data": None
        }
    
    return JsonResponse(response, status=200,safe=False)
