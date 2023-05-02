from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import *
from .models import *


# Create your views here.


def user_register(request):
    if request.method == "GET":
        return render(request, "user/register.html")
    if request.method == "POST":

        password = request.POST["password"]
        password_again = request.POST["password_again"]
        if password != password_again:
            return render(request, "user/register.html", {"password_error": "两次输入的密码不一致"})

        form = UserRegisterModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("user:user_login"))
        else:
            error = form.errors
            return render(request, "user/register.html", locals())


def user_login(request):
    if request.method == "GET":
        return render(request, "user/login.html")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data.get("userid")
            password = form.cleaned_data.get("password")
            user = authenticate(request, userid=userid, password=password)
            if user:
                login(request, user)
                # 这里不能使用render，要redirect
                return redirect("book:index")
            else:
                return render(request, "user/login.html", {"error": "用户名或密码错误"})
        else:
            error = form.errors
            return render(request, "user/login.html", locals())


def user_logout(request):
    logout(request)
    return redirect(reverse("user:user_login"))


def user_password(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = PasswordForm()
            return render(request, "user/user_password.html", locals())
        elif request.method == "POST":
            user = request.user
            form = PasswordForm(request.POST)
            if form.is_valid():
                origin_password = form.cleaned_data.get("origin_password")
                new_password = form.cleaned_data.get("new_password")
                is_true_password = check_password(origin_password, user.password)
                if not is_true_password:
                    return render(request, "user/user_password.html", {"password_error": "原密码不正确！"})
                user.set_password(new_password)
                user.save()
                return redirect(reverse("user:user_login"))
            else:
                errors = form.errors
                return render(request, "user/user_password.html", locals())
    else:
        return redirect("user:login")


def user_profile_view(request):
    user = request.user
    try:
        profile = user.user_profile
        print("hello")
        return render(request, "user/profile.html", locals())
    except Exception:
        profile = None
        return render(request, "user/profile.html", locals())


def user_profile_create(request):
    if request.method == "GET":
        form = ProfileModelForm()
        return render(request, "user/profile_create.html", locals())
    elif request.method == "POST":
        form = ProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("user:user_profile_view")
        else:
            errors = form.errors
            return render(request, "user/profile_create.html", locals())


class UserProfileUpdate(UpdateView):
    template_name = "user/profile_update.html"
    form_class = ProfileModelForm
    success_url = reverse_lazy("user:user_profile_view")
    queryset = UserProfile.objects.all()
