from django.urls import path
from . import views


app_name = 'auth'
urlpatterns = [
    path('sign-in', views.sign_in_page, name='signin'),
    path('sign-up', views.sign_up_page, name='signup'),
    path('sign-out', views.sign_out_page, name='signout'),
    path('enter-sms-code/<uidb64>/<token>', views.enter_sms_code, name='enter-sms-code'),
]