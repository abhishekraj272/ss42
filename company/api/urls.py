from django.urls import path
from  rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('register/', views.Company.as_view({'get': 'list', 'post': 'create'})),
    path('post/', views.PostViewSet.as_view({'get': 'list'})),
]
