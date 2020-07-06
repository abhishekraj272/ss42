import json
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework import mixins
from rest_framework_api_key.models import APIKey
from django.db import close_old_connections
from django.shortcuts import get_object_or_404

from company.api.serializers import CompanySerializer, CompanySerializer_read       # Importing serializer
from posts.api.serializers import PostSerializer_read
from company.models import Company                                                  # Importing models
from posts.models import Post
from django.contrib.auth.models import User
from rest_framework import filters

generic_emails = ['gmail', 'yahoo', 'rediff', 'outlook', 'yandex', 'aol', 'gmx', ]

class CompanyRead(viewsets.ModelViewSet):
    permission_classes =[HasAPIKey, ]
    authentication_classes =()
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        key = self.request.META['HTTP_API_KEY']
        company_name = APIKey.objects.get_from_key(key)
        company = User.objects.get(username=company_name)
        return self.queryset.filter(company_name=company)

    # def list(self, request, *args, **kwargs):
    #     key = request.META['HTTP_API_KEY']
    #     company = APIKey.objects.get_from_key(key)
    #     return Response({ "detail": "Method \"GET\" not allowed..." }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CompanyUpdate(viewsets.ModelViewSet):
    permission_classes =[HasAPIKey, ]
    authentication_classes =()
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        company_id = self.request.data['id']
        name = self.request.data['company_name']
        company_ = Company.objects.get(id=company_id)
        user_ = User.objects.get(username=company_.company_name)

        apikey_ = APIKey.objects.get(name=company_.company_name)
        apikey_.name = name
        apikey_.save()

        user_.username = name
        user_.save()

        return Response({"message": "Username updated !!"}, status=status.HTTP_200_OK)

class CompanyView(viewsets.ModelViewSet,mixins.UpdateModelMixin,):
    permission_classes =[]
    authentication_classes =()
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        i = self.request.data['email'].index('@')
        company_name = self.request.data['email'][i+1:]
        j = company_name.index('.')
        company_name = company_name[:j]

        if company_name in generic_emails:
            return Response({ "detail": "Please register with your company email !!" }, status=status.HTTP_403_FORBIDDEN)
        else:
            self.request.data["company_name"] = company_name

        if User.objects.filter(username=self.request.data["company_name"]):
            company_obj = User.objects.get(username=self.request.data["company_name"])
            if  self.queryset.get(company_name=company_obj):
                self.request.data["api_key"] = self.queryset.filter(company_name=company_obj)[0].api_key
                return Response({"message": "Already registered"}, status=status.HTTP_200_OK)
        else:
            print("Entered else")
            company = User.objects.create(username=self.request.data["company_name"])  
            company.set_password(self.request.data["password"])
            company.save()
            api_key, key = APIKey.objects.create_key(name=self.request.data['company_name'])
            self.request.data["api_key"] = str(key)

            return super(CompanyView, self).create(request)
        # serializer = self.get_serializer(data=request.data)
        # serializer = CompanySerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        company = User.objects.get(username=self.request.data["company_name"])
        serializer.save(company_name=company)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)   
    # # def put(self, request, pk=None, format=None):
    # #     snippet  = Company.objects.filter(pk=pk)
    # #     serializer = CompanySerializer_read(snippet, data=request.data)
    # #     if serializer.is_valid():
    # #         serializer.save()
    # #         return Response(serializer.data)
    # #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    #     # return Response({"method":"put"})
class PostViewSet(viewsets.ModelViewSet):
    close_old_connections()
    queryset = Post.objects.all()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['url']
    permission_classes =[HasAPIKey, ]
    authentication_classes =()
    serializer_class = PostSerializer_read
    close_old_connections()

