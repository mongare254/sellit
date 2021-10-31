
from django.urls import path
from .import views

app_name='user'
urlpatterns = [
    path('', views.landing, name='landings'),
    path('home', views.home, name='home'),
    path('login/', views.loginuser, name='login'),
    path('register/', views.registeruser, name='register'),
    path('checkuser',views.check_username_exist, name='checkuser'),
    path('checkemail',views.check_email, name='checkemail'),
    path('userdetails',views.checkdetails, name='checkdetails'),
    path('additem',views.additem, name='additem'),
    path('logout',views.logout_request, name='logout'),
    path('interested/<str:pk>',  views.interested, name="interested"),
    path('auctionroom/<str:pk>',views.auctionrooms, name='auctionroom'),
    path("send_otp",views.send_otp,name="send_otp"),
    path('interest/<str:pk>', views.interest, name="interest"),
    path('mybasket', views.mybasket, name="mybasket"),
    path('myitems', views.myitems, name="myitems"),
    path('deletebasket/<str:pk>', views.deletebasket, name="deletebasket"),
    path('deleteitem/<str:pk>', views.deleteitem, name="deleteitem"),
    path('payment', views.payment, name="payment"),
    path('auctionhandler', views.auctionroomshandler, name="auctionhandler"),
    path('sendwinnermail', views.sendwinnermail, name="winnermail")

]
