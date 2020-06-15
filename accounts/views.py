from django.shortcuts import render
from .forms import SignForm
from .models import Authentication
from accounts.models import signupModel
from django.contrib.auth.models import User
from django.http import HttpResponse
import pyotp
from django.core.mail import send_mail
# Create your views here.

def signuppage(request):
    return render(request,'register.html',{'data':SignForm()})


def saveregistrationdetails(request):
    uname = request.POST.get('username')
    email = request.POST.get('email')
    upass = request.POST.get('password')
    upass2 = request.POST.get('password2')
    signupModel(username=uname,email=email,password=upass,password2=upass2).save()
    return render(request,'register.html',{'message':'register succssfully'})

def create_verification(request, id):
    user = User.objects.get(id=id)
    if not user:
        return HttpResponse(status=401)

    ran = pyotp.random_base32()

    token = pyotp.totp.TOTP(ran).now()

    try:
        obj = Authentication.objects.get(user=id)
        obj.token = token
        obj.save()
    except Authentication.DoesNotExist:
        obj = Authentication(user=user, token=token)
        obj.save()
    
    
    
    if token:
        from_email = f'Scrapshut pythonautomail1@gmail.com'
        subject = 'Verify Your Email with Scrapshut'
        message = f'Copy and paste this url in your browser to verify https://backend.scrapshut.com/api/verify/confirm/{ran}/{id}/{token}'
        recepient = user.email
        print(recepient)
        try:
            send_mail(subject, message, from_email, [recepient], fail_silently = False)
        except Exception as e:
            HttpResponse(e, status=403)
    
    return HttpResponse(f'Verification link sent to your email :)',status=200)
    
def confirm_verification(request, id, otp, complex):
    user_auth = Authentication.objects.get(user=id)
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()

    if int(user_auth.token) == int(otp):
        user_auth.token = pyotp.totp.TOTP('abhishek').now()
        user_auth.save()
        return HttpResponse(f"Email successfully verified for {user.username} :)")
    


    return HttpResponse(f"OTP wrong. Please try again :(")
    
