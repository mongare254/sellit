
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

admin.site.site_title = "Sellme Admin Portal"
urlpatterns = [
    path('dadmin/', admin.site.urls),
    path('admin/', include('myadmin.urls')),
    path('', include('user.urls')),
    # path('mpesa/', include('mpesa.urls')),

    path('password_reset/', auth_views.PasswordChangeView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
