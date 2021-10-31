from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *
from mpesa.models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages as m
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
import math, random
from django.http import JsonResponse#json response
from django.core import serializers #serializing
from django.forms.models import model_to_dict #printing
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
def loginuser(request):
    if request.method =='POST':
        username=request.POST['username']
        password = request.POST['password']

        user=authenticate(username=username, password=password)
        if user is not  None:
            if user.is_superuser:
                login(request, user)
                return redirect('myadmin:dashboard')

            else:
                login(request, user)
                return redirect('user:home')
        else:
            m.error(request, 'Invalid User Credentials! Try again!')
            return render(request, 'user/login.html')
    else:
        return render(request, 'user/login.html')
def registeruser(request):
    if request.method =='POST':
        firstname=request.POST['firstname']
        secondname = request.POST['secondname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        identity = request.POST['id_no']
        phone = request.POST['phone']

        try:
            newuser=User.objects.create_user(username=username, email=email, password=password)
            newuser.profile.firstname=firstname
            newuser.profile.secondname = secondname
            newuser.profile.phone = phone
            newuser.profile.identityno = identity
            newuser.save()
            return render(request, 'user/login.html')
        except:
            return render(request, 'user/login.html')
    else:
        return render(request, 'user/login.html')

@login_required()
def home(request):
    items=item.objects.all().order_by('-id')
    return render(request, 'user/home.html', {'items':items})

def landing(request):
    return render(request, 'user/landingpage.html')

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=User.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_email(request):
    email=request.POST.get("email")
    email_obj=User.objects.filter(email=email).exists()
    if email_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def checkdetails(request):
    username=request.POST.get("username")
    user_obj=User.objects.filter(username=username).exists()

    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@login_required()
def additem(request):
    if request.method=='POST':
        item_name=request.POST.get('item_name')
        description=request.POST.get('description')
        item_image=request.FILES.get('item_image')
        item_id= request.POST.get('category')
        category=Category.objects.get(id=item_id)
        count=category.number+1
        username=request.POST.get('username')
        start_price = request.POST.get('starting_price')

        items=item(item_name=item_name, description=description, item_image=item_image, category=category, item_price=start_price)
        items.user = request.user
        items.save()
        category.number=count
        category.save()
        try:
            items.save()
            current_user = request.user.profile
            m.success(request, "Item added Successfully!")
            return render(request,'user/additem.html', {'cuser':current_user})
        except:
            current_user=request.user.profile
            return render(request,'user/additem.html', {'cuser':current_user})
    else:
        item_cat=Category.objects.all()
        current_user = request.user.profile
        return render(request, 'user/additem.html',{'cuser':current_user, 'items':item_cat})

def logout_request(request):
    logout(request)
    return redirect("user:login")

@login_required()
def interested(request,pk):
    current_item= item.objects.filter(id=pk)
    return render(request, 'user/interested.html', {'item': current_item})

@login_required()
def auctionroomshandler(request):
    if request.method =='POST':
        pk=request.POST.get('pk')
        all_items = item.objects.get(id=pk)
        amount=request.POST.get('amount')
        user_id=request.user.id
        current_item=all_items.item_name
        c_user= bidding.objects.get(id=user_id)
        c_user.amount_bid=amount
        c_user.save()
        bidders = bidding.objects.all().order_by('-amount_bid')
        highest_bidder = bidders[0]

        return render(request, 'user/auctionroom.html', {'bidders': bidders, 'highest_bidder': highest_bidder})
    else:
        a_item = item.objects.filter(id=pk)
        amount = request.POST.get('amount')
        username = request.user.username
        item_name = a_item.item_name
        c_user = bidding.objects.get(username=username)
        c_user.amount_bid = amount
        c_user.save()
        bidders = bidding.objects.all().order_by('-amount_bid')
        highest_bidder = bidders[0]
        return render(request, 'user/auctionroom.html', {'bidders': bidders, 'highest_bidder': highest_bidder})

def auctionrooms(request, pk):
    c_item=item.objects.filter(id=pk)
    return render(request, 'user/auctionroom.html',{'items':c_item})

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def deletebasket(request,pk):
    c_item=interested_item.objects.filter(id=pk)
    c_item.delete()
    m.success(request, 'Item deleted successfully')
    logged_user = request.user
    i_items = interested_item.objects.filter(username=logged_user)
    return render(request, 'user/mybasket.html', {'items':i_items})


def send_otp(request):
    email = request.POST.get("email")
    o = generateOTP()
    htmlgen = '<p>Your OTP is <strong>o</strong></p>'
    send_mail('OTP request',
    o, '<your gmail id>', [email], fail_silently=False, html_message=htmlgen)
    return HttpResponse(o)

def interest(request, pk):
    user = request.user
    a_payments = Succesful_Mpesa_payments.objects.filter(Paying_user=user)
    your_receipt = item.objects.get(id=pk)
    template_path = 'user/receipt.html'
    context = {'your_receipt': your_receipt, 'a_payments': a_payments}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="receipt.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required()
def myitems(request):
    logged_user = request.user
    m_items = item.objects.filter(user=logged_user)
    return render(request, 'user/myitems.html', {'items':m_items})

@login_required()
def mybasket(request):
    logged_user=request.user
    i_items=interested_item.objects.filter(username=logged_user)
    return render(request, 'user/mybasket.html', {'items': i_items})

@login_required()
def deleteitem(request,pk):
    c_item = item.objects.filter(id=pk)
    c_item.delete()
    m.success(request, 'Item deleted successfully')
    logged_user = request.user
    m_items = item.objects.filter(user=logged_user)
    return render(request, 'user/myitems.html', {'items': m_items})

def payment(request):
    logged_user = request.user
    s_payments = Succesful_Mpesa_payments.objects.filter(Paying_user=logged_user)
    u_payments=Unsuccesful_Mpesa_payments.objects.filter(Paying_user=logged_user)
    return render(request, 'user/payment.html', {'payments': s_payments,'failed_ps':u_payments})

def sendwinnermail(request):
    c_user=request.user.username
    subject = 'Payment received'
    message = f'Hi {c_user}, COngratulations You on the item!! Please pay the required bid amount within 24 hopurs'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [c_user.email]
    send_mail(subject, message, email_from, recipient_list)
    print(recipient_list)