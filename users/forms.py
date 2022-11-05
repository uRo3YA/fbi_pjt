from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from .models import Profile
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

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
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields["hp"].label = "연락처"
        self.fields["hp"].widget.attrs.update(
            {"class": "form-control", "autofocus": False}
        )
        self.fields["email"].label = "이메일"
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
            }
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
## 탈퇴시 비밀번호 체크 폼
class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error("password", "비밀번호가 일치하지 않습니다.")