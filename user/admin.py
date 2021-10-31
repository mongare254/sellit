from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(item)
admin.site.register(interested_item)
admin.site.register(payment)
admin.site.register(bidding)
admin.site.register(Category)