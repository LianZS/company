import random
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.cache import cache
from .send_email import send_email
from .forms import LoginForm, RegisterForm, ModifyForm


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
            return HttpResponseRedirect("/pinlianyou/manager")
        else:
            status = "error"

    else:
        form = LoginForm()

        return render(request, "login.html", {"form": form})


@csrf_exempt
def validation_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/pinlianyou/manager")
        else:
            status = "error"
    else:
        status = 'error'
    return JsonResponse({"status": status})


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
    注册界面
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        verification_code = request.POST['verification']  # 验证码
        right_verification_code = cache.get(email)
        if verification_code == right_verification_code:
            user = User.objects.create_user(username=username, password=password, email=email)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pinlianyou/manager')
        else:
            return HttpResponse('验证码有误')

    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def manager_veiw(request):
    """
    管理界面
    :param request:
    :return:
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.username
            company = "品联优"
            return render(request, 'manager.html', locals())
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def modify_password(request):
    """
    修改密码
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.POST['email']
        verification_code = request.POST['verification']  # 验证码
        right_verification_code = cache.get(email)
        if verification_code == right_verification_code:
            password = request.POST['password']

            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

        return HttpResponse("ok")
    else:
        form = ModifyForm()
    return render(request, "modify.html", {"form": form})


@csrf_exempt
def send_verification_view(request):
    """
    发送验证码邮件
    :param request:
    :return:
    """
    if request.method == "POST":
        verification_code = ''  # 验证码
        for i in range(5):
            verification_code += str(random.randint(0, 9))
        email_address = request.POST['email']
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
