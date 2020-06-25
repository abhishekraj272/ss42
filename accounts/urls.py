from .views import create_verification, confirm_verification, company_generate_otp, company_otp_verify
from django.urls import path

urlpatterns = [
    path('create/<int:id>', create_verification),
    path('confirm/<str:complex>/<int:id>/<int:otp>', confirm_verification),
    path('company/create/<int:id>', company_generate_otp),
    path('company/confirm/<str:complex>/<int:id>/<int:otp>', company_otp_verify),
]
