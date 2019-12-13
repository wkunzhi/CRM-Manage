# by 362416272@qq.com
from django import forms
from django.core.exceptions import ValidationError
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from stark.service.v1 import StarkHandler, get_choice_text, StarkModelForm, StarkForm, Option
from web import models
from web.utils.MD5 import gen_md5
from .base import PermissionHandler  # 粒度控制


class UserInfoAddModelForm(StarkModelForm):
    """
    新增页面
    修改字段显示顺序， 添加页面多加一个 确认密码
    自定义展示顺序，因为原理用的ModelForm，所以这里直接引用修改即可
    """
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']

    # 密码不一致，定制钩子方法
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        """钩子方法原始form表单验证中的，密码搞为密文的"""
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)  # md5加密再返回
        return self.cleaned_data


# 用户
class UserInfoEditModelForm(StarkModelForm):
    """
    修改信息页面
    修改字段显示顺序， 删除密码显示
    """

    class Meta:
        model = models.UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class ResetPasswordForm(StarkForm):
    # 继承stark的基类
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    # 密码不一致，定制钩子方法
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        """钩子方法原始form表单验证中的，密码搞为密文的"""
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)  # md5加密再返回
        return self.cleaned_data


class UserInfoHandler(PermissionHandler, StarkHandler):

    def display_reset_pwd(self, obj=None, is_header=None, *args, **kwargs):  # 自定义额外字段，然后加到list_display中即可
        if is_header:
            return '重置密码'
        reset_url = self.reverse_commons_url(self.get_url_name('rest_pwd'), pk=obj.pk)  # 带上id 反向生成别名
        return mark_safe('<a href="%s" class="layui-btn layui-btn-primary layui-btn-sm">重置密码</a>' % reset_url)

    list_display = ['nickname', get_choice_text('性别', 'gender'), 'phone', 'email', 'depart', display_reset_pwd]
    # 加上模糊搜索
    search_list = ['nickname__contains', 'name__contains']
    # 加上组合搜索
    search_group = [
        Option(field='gender'),
        Option(field='roles', is_multi=True),
    ]

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoEditModelForm

# 扩展功能==================单独一个url处理重置密码功能==================

    # 自定义的视图函数，给下面调用
    def reset_password(self, request, pk):
        """重置密码的视图函数"""
        user_object = models.UserInfo.objects.filter(id=pk).first()
        if not user_object:
            return HttpResponse('用户不存在无法重置密码')
        if request.method == 'GET':
            form = ResetPasswordForm
            return render(request, 'stark/change.html', {'form': form})
        # 校验保存
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            # 密码更新到数据库
            user_object.password = form.cleaned_data['password']
            user_object.save()
            return redirect(self.reverse_list_url())  # 直接使用封装好的方法，会跳页面
        return render(request, 'stark/change.html', {'form': form})

    # 自定义增加url（重置密码）用写好的钩子方法
    def extra_urls(self):
        patterns = [
            url(r'^reset/password/(?P<pk>\d+)$', self.wrapper(self.reset_password), name=self.get_url_name('rest_pwd'))
        ]
        return patterns
