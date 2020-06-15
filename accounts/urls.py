from .views import create_verification, confirm_verification
from django.urls import path

urlpatterns = [
    path('create/<int:id>', create_verification),
    path('confirm/<str:complex>/<int:id>/<int:otp>', confirm_verification),
]
