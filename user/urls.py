from django.urls import path, include
from .views import *
from .manager_view import *

urlpatterns = [
    path("login", login_view),
    path("verification", validation_user),

    path("register", registered_view),
    path("forget", loginout_view),
    path("sendVerificationCode", send_verification_view),
    path("modify", modify_password),
    path("manager/", include([
        path('', manager_veiw),
        path('recruitment', manager_recruitment),

    ])),
    path('recruitmentpage/<slug:uid>', recruitmentpage),
    path('apply/<slug:uid>', apply_view),
]
