import random
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.cache import cache
from .send_email import send_email
from .forms import LoginForm, RegisterForm


# Create your views here.
@csrf_exempt
def login_view(request):
    """
    登陆界面
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

        return HttpResponse("ok")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def loginout_view(request):
    """

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("loginout success")
    return HttpResponse("账号未登陆")


@csrf_exempt
def registered_view(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

        return HttpResponse("ok")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def send_email_view(request):
    if request.method == "GET":
        verification_code = ''  # 验证码
        for i in range(5):
            verification_code += str(random.randint(0, 9))
        email_address = request.GET['email']
        subject = verification_code + "是你的验证码"
        from_emial = 'publiccomany<publiccomany@163.com>'
        to_email = email_address

        message = "这事你的验证码:" + verification_code
        html_content = "<html><p>确认你的邮件地址 在创建账号之前，你需要完成一个简单的步骤。让我们确保这是正确的邮件地址" \
                       " — 请确认这是用于你的新账号的正确地址。 请输入此验证码以开始使用 ：</p>" \
                       "<strong style='color:blue;font-size:30px'>{code}</strong> " \
                       "<p>验证码两小时后过期。 谢谢！</p></html>".format(code=verification_code)
        send_email.delay(EmailMultiAlternatives, from_emial, to_email, subject, message, html_content,
                         verification_code, cache)

    return HttpResponse("success")
