from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User

from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model, update_session_auth_hash

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    users = User.objects.all()
    # Template에 전달한다.
    context = {"users": users}
    return render(request, "users/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ModelForm의 save 메서드의 리턴값은 해당 모델의 인스턴스다!
            auth_login(request, user)  # 로그인
            return redirect("root")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "users/signup.html", context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {"user": user}
    return render(request, "users/detail.html", context)


def login(request):
    if request.method == "POST":
        # AuthenticationForm은 ModelForm이 아님!
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            auth_login(request, form.get_user())

            return redirect(request.GET.get("next") or "root")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "users/login.html", context)


def logout(request):
    auth_logout(request)
    messages.warning(request, "로그아웃 하였습니다.")
    return redirect("root")


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "users/update.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 세션 무효화 방지
            update_session_auth_hash(request, form.user)
            return redirect("users:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "users/change_password.html", context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("root")
