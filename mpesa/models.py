from django.db import models
from user.models import Profile,item
from  django.contrib.auth.models import User


# a model for storing mpesa responses
class Mpesa_api_Responses(models.Model):
    MerchantRequestID = models.CharField(max_length=50)
    CheckoutRequestID = models.CharField(max_length=50)
    ResponseCode = models.IntegerField()
    ResponseDescription = models.TextField()
    CustomerMessage = models.TextField()
    the_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    paid_item=models.ForeignKey(item, on_delete=models.CASCADE,null=True, blank=True)

    class Meta:
        verbose_name = 'Mpesa Response'
        verbose_name_plural = 'Mpesa Responses'

    def __str__(self):
        return self.MerchantRequestID + ' ' + self.ResponseDescription


# model for succesful mpesa payments
class Succesful_Mpesa_payments(models.Model):
    MerchantRequestID = models.CharField(max_length=50)
    CheckoutRequestID = models.CharField(max_length=50)
    ResultCode = models.IntegerField()
    ResultDesc = models.TextField()
    Amount = models.DecimalField(decimal_places=3, max_digits=213)
    MpesaReceiptNumber = models.CharField(max_length=50)
    Balance = models.DecimalField(decimal_places=3, max_digits=213, blank=True, null=True)
    TransactionDate = models.DateTimeField()
    PhoneNumber = models.CharField(max_length=20)
    Paying_user =models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    Paid_item = models.ForeignKey(item, on_delete=models.CASCADE, null=True, blank=True)
    payment_for = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Succesful Mpesa Payment'
        verbose_name_plural = 'Succesful Mpesa Payments'

    def __str__(self):
        return self.payment_for , ' ' ,self.Paying_user


# model for unsuccesful mpesa payments
class Unsuccesful_Mpesa_payments(models.Model):
    MerchantRequestID = models.CharField(max_length=50)
    CheckoutRequestID = models.CharField(max_length=50)
    ResultCode = models.IntegerField()
    ResultDesc = models.TextField()
    Paying_user =models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Paid_item = models.ForeignKey(item, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name = 'unsuccesful Mpesa transaction'
        verbose_name_plural = 'unsuccesful Mpesa transactions'

    def __str__(self):
        return self.MerchantRequestID + ' ' + self.Paying_user

