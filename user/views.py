from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm
from django.contrib.auth.models import User


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
        loginout_view(request)
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
        form = LoginForm()
    return render(request, "login.html", {"form": form})
