# create: '2018/12/14' - 362416272@qq.com  
from django.core.exceptions import ValidationError

from django import forms
from rbac import models


class UserModelForm(forms.ModelForm):
    """ModelForm自动渲染form的类，便于下面调用"""
    # 第二次密码确认！！自定义一个字段
    confirm_password = forms.CharField(label='确认密码')

    class Meta:

        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

        # 调用bootCSS  给加上class=''即可  自定义样式！
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'confirm_password': forms.PasswordsInput(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        """高效统一添加样式"""
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # 钩子方法，做密码确认验证
    def clean_confirm_password(self):
        """检测密码是否一致"""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            # 固定语法：抛出异常
            raise ValidationError('两次输入不一致')


class UpdateUserModelForm(forms.ModelForm):
    """修改用户信息表单（没有密码和确认密码）"""

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        """高效统一添加样式"""
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResetPasswordUserModelForm(forms.ModelForm):
    """修改用户信息表单（没有密码和确认密码）"""
    # 第二次密码确认！！自定义一个字段
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        """高效统一添加样式"""
        super(ResetPasswordUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # 钩子方法，做密码确认验证
    def clean_confirm_password(self):
        """检测密码是否一致"""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            # 固定语法：抛出异常
            raise ValidationError('两次输入不一致')