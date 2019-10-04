from django.urls import path, include
from .views import *

urlpatterns = [
    path("login", login_view),
    path("register", registered_view),
    path("forget", loginout_view),
    path("sendmail", send_email_view),

]
