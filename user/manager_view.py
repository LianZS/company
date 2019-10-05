import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .forms import RecruitmentForm, LoginForm, AppliactionForm
from .models import Recruitment, ApplicantModel


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

            return render(request, 'manager_recruitment.html', {'form': form, 'create_time': datetime.datetime.now()})
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = RecruitmentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']  # 招聘标题
            low_remuneration = form.cleaned_data['low_remuneration']  # 最低报酬
            high_remuneration = form.cleaned_data['high_remuneration']  # 最高报酬
            recruit_num = form.cleaned_data['recruit_num']  # 招收人数
            experience = form.cleaned_data['experience']  # 经验要求
            record_schooling = form.cleaned_data['record_schooling']  # 学历要求
            gender = form.cleaned_data['gender']  # 性别
            contact_phone = form.cleaned_data['contact_phone']  # 联系方式
            work_address = form.cleaned_data['work_address']  # 工作地点
            position_describe = form.cleaned_data['position_describe']  # 岗位职责
            job_specification = form.cleaned_data['job_specification']  # 任职要求
            salary_specification = form.cleaned_data['salary_specification']  # 工资薪资
            welfare_treatment = form.cleaned_data['welfare_treatment']  # 福利待遇
            create_time = datetime.datetime.now()  # 创建时间
            recruitment_info = Recruitment.objects.create(title=title, low_remuneration=low_remuneration,
                                                          high_remuneration=high_remuneration, recruit_num=recruit_num,
                                                          experience=experience, record_schooling=record_schooling,
                                                          gender=gender,
                                                          contact_phone=contact_phone, work_address=work_address,
                                                          position_describe=position_describe,
                                                          job_specification=job_specification,
                                                          salary_specification=salary_specification,
                                                          welfare_treatment=welfare_treatment,
                                                          create_time=create_time)

            recruitment_info.save()
            uid = str(recruitment_info.id).replace("-", "")
            return HttpResponseRedirect('/pinlianyou/recruitmentpage/' + uid)
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

    return render(request, 'recruitment_page.html', {'recruitment_info': recruitment_info})


def apply_view(request, uid):
    """
    申请职位界面
    :param request:
    :param uid:
    :return:
    """
    form = AppliactionForm()
    try:
        work_name = Recruitment.objects.get(id=uid).title  # 岗位名称
    except ValidationError:
        raise Http404("Poll does not exist")
    return render(request, "application.html", {"form": form, "work_name": work_name})
