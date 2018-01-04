
import re

from django import forms

from .models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        # exclude = ('add_time',)
        # fields = '__all__'
        fields = ['name', 'mobile', 'course_name']

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
            raise forms.ValidationError("手机号码验证失败")


