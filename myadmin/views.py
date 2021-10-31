from django.shortcuts import render
from user.models import *
from mpesa.models import *
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def dashboard(request):
    items=item.objects.all().count()
    users=User.objects.all().count()
    payments=Succesful_Mpesa_payments.objects.all().count()
    c_users=User.objects.all()
    c_items=item.objects.all()
    c_payments=Succesful_Mpesa_payments.objects.all()
    return render(request, 'myadmin/dashboard.html', {'items':items, 'c_users':c_users, 'c_payments':c_payments,'users':users,'payments':payments})

def adduser(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        secondname = request.POST['secondname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        identity = request.POST['id_no']
        phone = request.POST['phone']

        try:
            newuser = User.objects.create_user(username=username, email=email, password=password)
            newuser.profile.firstname = firstname
            newuser.profile.secondname = secondname
            newuser.profile.phone = phone
            newuser.profile.identityno = identity
            newuser.save()

            messages.success(request, 'User Added Successfully')
            return render(request, 'myadmin/adduser.html')
        except:
            messages.error(request, 'Unable to Add user')
            return render(request, 'myadmin/adduser.html')

    else:
        return render(request, 'myadmin/adduser.html')

def additem(request):
    return render(request, 'myadmin/additem.html')