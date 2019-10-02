from django.shortcuts import render, HttpResponse
from .forms import LoginForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponse("ok")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})
