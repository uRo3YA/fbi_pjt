from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django import forms
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("last_name","first_name","username", "password1", "password2", "email")
        labels = {
            "last_name":"성",
            "first_name":"이름",
            "username": "아이디",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "email": "이메일",
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]