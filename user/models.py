from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import timedelta
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50, null=True)
    secondname=models.CharField(max_length=50, null=True)
    identityno=models.IntegerField(null=True)
    phone=models.IntegerField(null=True)
    profile_image=models.ImageField(upload_to='profilepics', blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):
    title = models.CharField(max_length=225)
    number=models.IntegerField(default=0)
    # slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Category_title', args=(self.id,))

    @property
    def get_products(self):
         return item.objects.filter(category=self.title)

class item(models.Model):

    def return_date_time():
        now = timezone.now()
        return now + timedelta(days=3)

    item_name=models.CharField(max_length=50)
    item_price=models.FloatField()
    item_image=models.ImageField(upload_to='images/', blank=True)
    description=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    approval_status=models.CharField(max_length=50, default="Waiting")
    auction_status=models.CharField(max_length=50, default="Scheduled")
    date_added=models.DateTimeField(auto_now=True)
    date_scheduled=models.DateTimeField(default=return_date_time)
    category=models.ForeignKey(Category, blank=True,related_name='Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name

    def get_time_diff(self):
        if self.date_scheduled:
            now = timezone.now()
            timediff = self.date_scheduled-now
            timedifference = timediff.total_seconds()/3600
            return timedifference

            if timedifference <=0:
                self.auction_status='Active'


class interested_item(models.Model):
    item_name=models.ForeignKey(item, blank=True, on_delete=models.CASCADE)
    username=models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    date_paid = models.DateTimeField(null=True)

    def __str__(self):
        return self.item_name ,' ', self.username

class payment(models.Model):
    item_name=models.ForeignKey(item, blank=True, on_delete=models.CASCADE)
    username=models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    pay_for=models.CharField(max_length=50)
    date_paid=models.DateTimeField(null=True)

    def __str__(self):
        return self.item_name,' ', self.username

class bidding(models.Model):
    item_name=models.ForeignKey(item, blank=True, on_delete=models.CASCADE)
    username=models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    amount_bid=models.FloatField(max_length=50)

    def __str__(self):
        return self.username
