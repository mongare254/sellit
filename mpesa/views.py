from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages as m
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
import requests
from requests.auth import HTTPBasicAuth
import json
from . credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import *
from user.models import *
import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from sellme.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.conf import settings

def itempayment(request):
    if request.method == 'POST':
        username = request.user
        p_number = request.POST.get('phone')
        item_id=request.POST.get('item_id')
        amount= '1'

        pay_for="Registration"
        items=item.objects.get(id=item_id)
        date_time=make_aware(datetime.datetime.now())

        # call_back_url = "https://d5ed064aad2b.ngrok.io //mpesa/callback"
        access_token = MpesaAccessToken.validated_mpesa_access_token

        print(access_token)
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA":p_number,  # replace with your phone number to get stk push
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": p_number,  # replace with your phone number to get stk push
            "CallBackURL": "https://wicked-panther-58.loca.lt/mpesa/callback",
            "AccountReference": "Nisisi Technologies",
            "TransactionDesc": "Item Registration"
        }

        response = requests.post(api_url, json=request, headers=headers)
        response_data = response.json()
        print(response_data)

        Merchant_RequestID = response_data["MerchantRequestID"]
        Checkout_RequestID = response_data["CheckoutRequestID"]
        Response_Code = response_data["ResponseCode"]
        Response_Description = response_data["ResponseDescription"]
        Customer_Message = response_data["CustomerMessage"]

        try:
            add_bidding=bidding(item_name=items,username=username, amount_bid=0)
            add_interest = interested_item(item_name=items, username=username, date_paid=date_time)
            item_payment = payment(item_name=items, username=username, pay_for=pay_for, date_paid=date_time)
            add_interest.save()
            item_payment.save()
            add_bidding.save()
            saving_response = Mpesa_api_Responses(
                MerchantRequestID=Merchant_RequestID,
                CheckoutRequestID=Checkout_RequestID,
                ResponseCode=Response_Code,
                ResponseDescription=Response_Description,
                CustomerMessage=Customer_Message,
                the_user=username,
                paid_item=items

            )
            saving_response.save()
            return redirect('user:interested', pk=item_id)
        except Exception as e:
            print('%s (%s)' % (e.message, type(e)))

        if Response_Code == '0':
            m.success(request, 'Please enter the Mpesa Pin on Your Phone')
            return redirect('user:interested', pk=item_id)

        else:
            m.error(request, 'Payment failed!! try again or contact administrator')
            return redirect('user:interested', pk=item_id)

    else:
        return redirect('user:interested', pk=item_id)

@csrf_exempt
def call_back(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    print(mpesa_body)
    print(mpesa_payment)

    Merchant_RequestID = mpesa_payment['Body']['stkCallback']['MerchantRequestID']
    mpesa_response = Mpesa_api_Responses.objects.get(MerchantRequestID=Merchant_RequestID)
    paid_item_name=mpesa_response.paid_item
    paying_user=mpesa_response.the_user
    c_user=User.objects.get(username=paying_user.username)
    Checkout_RequestID = mpesa_payment['Body']['stkCallback']['CheckoutRequestID']
    Result_Code = mpesa_payment['Body']['stkCallback']['ResultCode']
    pay_for = "Registration"
    if Result_Code == 0:
        Result_Desc = mpesa_payment['Body']['stkCallback']['ResultDesc']
        Amount = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        Mpesa_ReceiptNumber = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        # Balance = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value']
        Transaction_Date = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        str_transaction_date = str(Transaction_Date)
        transaction_datetime = datetime.datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
        Phone_Number = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']

        #send  mail
        try:
            subject = 'Payment received'
            message = f'Hi {c_user}, Your payment has been received of { Amount} was received on {Transaction_Date}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [c_user.email]
            send_mail(subject, message, email_from, recipient_list)
            print(recipient_list)

        except:
            print("Error!")

        payment = Succesful_Mpesa_payments(
            MerchantRequestID=Merchant_RequestID,
            CheckoutRequestID=Checkout_RequestID,
            ResultCode=Result_Code,
            Amount=Amount,
            ResultDesc=Result_Desc,
            MpesaReceiptNumber=Mpesa_ReceiptNumber,
            # Balance = Balance,
            TransactionDate=transaction_datetime,
            PhoneNumber=Phone_Number,
            Paying_user=paying_user,
            Paid_item=paid_item_name,
            payment_for=pay_for
        )
        payment.save()
        m.success(request, 'Your payment has been received')

    else:
        p_username = request.user
        # p_number = request.POST.get('phone')
        item_id = request.POST.get('item_id')
        items = item.objects.get(id=item_id)
        Result_Desc = mpesa_payment['Body']['stkCallback']['ResultDesc']
        unsuccesful_payment = Unsuccesful_Mpesa_payments(
            MerchantRequestID=Merchant_RequestID,
            CheckoutRequestID=Checkout_RequestID,
            ResultCode=Result_Code,
            ResultDesc=Result_Desc,
            Paid_item=items,
            Paying_user=p_username
        )
        unsuccesful_payment.save()
        m.error(request, 'Your payment is not succesful,Transaction cancelled by user!!!')



    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))
    """b'{"Body":{"stkCallback":
    {"MerchantRequestID":"110340-19624580-1",
    "CheckoutRequestID":"ws_CO_230320212143567814",
    "ResultCode":0,
    "ResultDesc":"The service request is processed successfully.",
    "CallbackMetadata":
    {"Item":[{"Name":"Amount","Value":1.00},
    {"Name":"MpesaReceiptNumber","Value":"PCN91BO4H7"},
    {"Name":"Balance"},{"Name":"TransactionDate","Value":20210323214413},
    {"Name":"PhoneNumber","Value":254721480230}]}}}}'"""
    # print(request.body, "this is request data")
    # return HttpResponse(response.text)
    '''
    {"Body":{"stkCallback":{"MerchantRequestID":"18982-23012932-1",
    "CheckoutRequestID":"ws_CO_240320212324024921",
    "ResultCode":1032,"
    ResultDesc":"Request cancelled by user"}}}
{'Body': {'stkCallback': {'MerchantRequestID': '18982-23012932-1', 'CheckoutRequestID': 'ws_CO_240320212324024921', 'ResultCode': 1032, 'ResultDesc': 'Request cancelled by user'}}}
    '''


