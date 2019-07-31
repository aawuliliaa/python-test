from django.shortcuts import render,redirect,reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from untitled import settings
def chat(request):
    return render(request, 'index.html')
def login(request):
    # User.objects.create_user(username="vita", password="123")
    if request.method=="POST":
        user = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=user, password=password)
        print("mmmmmmmmmm",user)
        if user:
            auth.login(request, user)
        return redirect(reverse('tail'))
    return render(request,'login.html')


@login_required(login_url='/login/')
def tail(request):
    log_paths = settings.LOG_PATH
    return render(request, "tail.html", locals())