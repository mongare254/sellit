from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'mpesa'

urlpatterns = [
    #online payment urls
    # path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    # path('payitem', views.itempayment, name='payitem'),
    # path('callback', views.call_back, name="call_back"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)