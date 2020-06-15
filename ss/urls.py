"""ss URL Configuration


Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from core.views import IndexTemplateView
from  rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls.static import static
from django.conf import settings
# from django_registration.backends.one_step.views import RegistrationView
# from django_registration.backends.one_step import RegistrationView
# from django_registration.backends.one_step.views import RegistrationView

# from django_registration.one_step.views import RegistrationView
# from users.forms import CustomUserForm
from accounts import views

urlpatterns = [
    path('signup', views.signuppage),
    path('savedetails/',views.saveregistrationdetails,name='savedetails'),
    path('user/', include('objects.api.urls')),

    path('admin/', admin.site.urls),
    # path('auth/',n_auth_token),

    path('login', obtain_jwt_token, name='token_obtain_pair'),
    path('dev/', include('developer.urls')),
    path('company/', include('company.api.urls')),
    path('notification/', include('notification.urls')),
    path('notification/api/', include('notification.api.urls')),

    path('api/', include('posts.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/auth/', include('rest_framework_social_oauth2.urls')),
    path('a/', include('ss.api.urls')),

    path('api/payment/', include('payments.api.urls')),
    path('api/verify/', include('accounts.urls'))


    # path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    # re_path(r'^.*$',IndexTemplateView.as_view(),name='entry point')





]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
