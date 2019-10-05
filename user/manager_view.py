from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .forms import RecruitmentForm, LoginForm
from .models import Recruitment


@csrf_exempt
def manager_recruitment(request):
    """
    招聘管理
    :param request:
    :return:
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            form = RecruitmentForm()
            return render(request, 'recruitment.html', {'form': form})
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = RecruitmentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"result": "success"})
        else:
            return JsonResponse({"result": "fail"})


def recruitmentpage(request, uid):
    """
    招聘信息详情界面
    :param request:
    :param uid:
    :return:
    """
    try:
        recruitment_info = Recruitment.objects.get(id=uid)
    except ValidationError:
        raise Http404("Poll does not exist")

    return render(request, 'recruitmentpage.html', {'recruitment_info': recruitment_info})
