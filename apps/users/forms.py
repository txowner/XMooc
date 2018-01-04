import re

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ForgetpwdForm(forms.Form):
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': "验证码错误"})


class ResetpwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UserImageForm(forms.ModelForm):
    """
    用户头像 上传验证的 form
    """
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """
    更新 用户 常见的信息
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']

    def clean_mobile(self):
        """
        对 mobile 字段的值进行验证。 要验证那个字段， 就实现 clean_field_name 这个方法，实例化ModelForm的时候就会自动执行      
        """
        # 在 modelform中，实例化时会在对象内把所有变量生成一个名叫cleaned_data字典
        mobile = self.cleaned_data['mobile']
        regex = "^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$"
        pattern = re.compile(regex)
        if pattern.match(mobile):
            return mobile
        else:
            # 若这里出错，raise的error在验证(is_valid)时，会放到errors里面
            raise forms.ValidationError("手机号码验证失败")