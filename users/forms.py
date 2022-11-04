from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from .models import Profile
from django import forms
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("last_name","first_name","username", "password1", "password2", "hp","email")
        labels = {
            "last_name":"성",
            "first_name":"이름",
            "username": "아이디",
            "hp":"연락처",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "email": "이메일",
        }

class CustomUserChangeForm(UserChangeForm):
    hp = forms.IntegerField(
        label="연락처",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "maxlength": "11",
                "oninput": "maxLengthCheck(this)",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("hp" ,"email")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]

# 비밀번호 변경 폼
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].label = "기존 비밀번호"
        self.fields["old_password"].widget.attrs.update(
            {"class": "form-control", "autofocus": False}
        )
        self.fields["new_password1"].label = "새 비밀번호"
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["new_password2"].label = "새 비밀번호 확인"
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )