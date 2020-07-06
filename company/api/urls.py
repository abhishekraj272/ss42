from django.urls import path
from  rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('register/', views.CompanyView.as_view({'post': 'create'})),
    path('update/', views.CompanyUpdate.as_view({'put': 'update'})),      
    path('view/', views.CompanyRead.as_view({'get': 'list'})),
    path('post/', views.PostViewSet.as_view({'get': 'list'})),
]
