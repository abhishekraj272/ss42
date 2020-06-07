import json
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import JsonResponse, HttpResponse
from rest_framework import status

from rest_framework_api_key.models import APIKey
from django.db import close_old_connections

from company.api.serializers import CompanySerializer, CompanySerializer_read       # Importing serializer
from posts.api.serializers import PostSerializer_read
from company.models import Company                                                  # Importing models
from posts.models import Post

generic_emails = ['gmail', 'yahoo', 'rediff', 'outlook', 'yandex', 'aol', 'gmx', ]

class CompanyRead(viewsets.ModelViewSet):
    permission_classes =[HasAPIKey, ]
    authentication_classes =()
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        key = self.request.META['HTTP_API_KEY']
        company = APIKey.objects.get_from_key(key)
        return self.queryset.filter(company_name=company)

    # def list(self, request, *args, **kwargs):

    #     key = request.META['HTTP_API_KEY']
    #     company = APIKey.objects.get_from_key(key)
    #     return Response({ "detail": "Method \"GET\" not allowed..." }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class Company(viewsets.ModelViewSet):
    permission_classes =[]
    authentication_classes =()
    serializer_class = CompanySerializer_read
    queryset = Company.objects.all()

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        i = self.request.data['email'].index('@')
        company_name = self.request.data['email'][i+1:]
        j = company_name.index('.')
        company_name = company_name[:j]

        if company_name in generic_emails:
            return Response({ "detail": "Please register with your company email !!" }, status=status.HTTP_403_FORBIDDEN)

        self.request.data["company_name"] = company_name

        if  self.queryset.filter(company_name=company_name):
            print(True)
            self.request.data["api_key"] = self.queryset.filter(company_name=company_name)[0].api_key
        else:
            print(False)
            api_key, key = APIKey.objects.create_key(name=self.request.data['company_name'])
            self.request.data["api_key"] = str(key)
        # serializer = self.get_serializer(data=request.data)
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PostViewSet(viewsets.ModelViewSet):
    close_old_connections()
    queryset = Post.objects.all()
    search_fields = ['url']
    permission_classes =[HasAPIKey, ]
    authentication_classes =()
    serializer_class = PostSerializer_read
    close_old_connections()

