import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from company.models import Company

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username):
            company_obj = User.objects.get(username=username)
            if authenticate(username=username, password=password):
                api_key = Company.objects.filter(company_name=company_obj)[0].api_key
                return JsonResponse({"API Key": api_key}, status=status.HTTP_200_OK)
            else:
               return JsonResponse({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return JsonResponse({"error": "No user with this username found"}, status=status.HTTP_400_BAD_REQUEST)


