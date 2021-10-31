from django.contrib import admin
from .models import *

admin.site.site_header = "Sellme Admin"
admin.site.index_title = "Welcome to Sellme Admin"
admin.site.site_title = "Sellme Admin"
# Register your models here.
admin.site.register(Unsuccesful_Mpesa_payments)
admin.site.register(Succesful_Mpesa_payments)
admin.site.register(Mpesa_api_Responses)