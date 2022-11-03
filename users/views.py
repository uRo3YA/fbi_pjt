from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm ,ProfileForm
from .models import User
from .models import Profile
from Restaurant.models import Restaurant
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
        profile_ = Profile()  
        if form.is_valid():
            user = form.save()
            profile_.user = user # 프로필에 유저 추가
            profile_.save()      # 저장
            auth_login(request, user) 
            return redirect("users:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "users/signup.html", context)


def detail(request, pk):
    # print(a)
    user = get_user_model().objects.get(pk=pk)
    profile_ = user.profile_set.all()[0]
    a=(user.user_wishlist.all())
    #print(a.title)
    context = {
        "user": user,
        "profile": profile_,
        'user_wishlist': user.user_wishlist.all(),
        }
    return render(request, "users/detail.html", context)

def wishlist(request, pk):
    user = get_user_model().objects.get(pk=pk)
    profile_ = user.profile_set.all()[0]
    #a=(user.user_wishlist.all())
    #print(a.title)
    context = {
        "user": user,
        "profile": profile_,
        'user_wishlist': user.user_wishlist.all(),
        }
    return render(request, "users/wishlist.html", context)

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
    user_ = get_user_model().objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user) 
        if form.is_valid():
            form.save()
            #profile_form.save()
            return redirect("users:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form,}
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



@login_required
def profile_update(request):
    user_ = get_user_model().objects.get(pk=request.user.pk)
    current_user = user_.profile_set.all()[0]
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect("users:detail", request.user.pk)
    else:
        form = ProfileForm(instance=current_user)
    context = {
        "profile_form": form,
    }
    return render(request, "users/profile_update.html", context)

# def follow(request, pk):
#   user = get_user_model().objects.get(pk=pk)

#   if request.user != user:
#     if request.user not in user.wished_users.all():
#       user.wished_users.add(request.user)
#       is_following = True
#     else:
#       user.wished_users.remove(request.user)
#       is_following = False

#   data = {
#     'isFollowing': is_following,
#     'followers': user.followers.all().count(),
#     'followings': user.followings.all().count(),
#   }

#   return JsonResponse(data)
        
