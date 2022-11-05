from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm ,ProfileForm,CustomPasswordChangeForm,CheckPasswordForm
from .models import User
#from .models import Profile
from Restaurant.models import Restaurant
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.http import JsonResponse
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
        #profile_ = Profile()  
        if form.is_valid():
            user = form.save()
            #profile_.user = user # 프로필에 유저 추가
            #profile_.save()      # 저장
            auth_login(request, user) 
            return redirect("users:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "users/signup.html", context)

@login_required
def detail(request, pk):
    # print(a)
    user = get_user_model().objects.get(pk=pk)
    profile_ = user.image
    #followings=user.followers.all()
    #a=(user.user_wishlist.all())
    #print(followings.count)
    follower=get_user_model().objects.filter(followers=pk)
    #print(follower)
    context = {
        "user": user,
        "profile": profile_,
        'user_wishlist': user.user_wishlist.all(),
        'follower_list':follower
        }
    return render(request, "users/detail.html", context)

def wishlist(request, pk):
    user = get_user_model().objects.get(pk=pk)
    #profile_ = user.profile_set.all()[0]
    #a=(user.user_wishlist.all())
    #print(a.title)
    context = {
        "user": user,
        #"profile": profile_,
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
            messages.success(request, "회원정보가 수정되었습니다.")
            return redirect("users:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form, "data":user_}
    return render(request, "users/update.html", context)




@login_required
def change_password(request):
    if request.method == "POST":
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            # logout(request)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('root')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(
        request,
        "users/change_password.html",
        {"password_change_form": password_change_form},
    )


@login_required
def delete(request):
    if request.method == "POST":
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect("root")
    else:
        password_form = CheckPasswordForm(request.user)

    return render(
        request, "users/delete.html", {"password_form": password_form}
    )


@login_required
def profile_update(request):
    user_ = get_user_model().objects.get(pk=request.user.pk)
    #current_user = user_.profile_set.all()[0]
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_)
        if form.is_valid():
            form.save()
            return redirect("users:detail", request.user.pk)
    else:
        form = ProfileForm(instance=user_)
    context = {
        "profile_form": form,
    }
    return render(request, "users/profile_update.html", context)

@login_required
def follow(request, pk):
    # 프로필에 해당하는 유저를 로그인한 유저가!
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user == user:
        messages.warning(request, '스스로 팔로우 할 수 없습니다.')
        return redirect('users:detail', pk)
    if request.user in user.followers.all():
    # (이미) 팔로우 상태이면, '팔로우 취소'버튼을 누르면 삭제 (remove)
        user.followers.remove(request.user)
    else:
    # 팔로우 상태가 아니면, '팔로우'를 누르면 추가 (add)
        user.followers.add(request.user)
    return redirect('users:detail', pk)