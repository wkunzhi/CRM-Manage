# create: '2018/12/14' - 362416272@qq.com  
from django import forms
from rbac import models


class RoleModelForm(forms.ModelForm):
    """ModelForm自动渲染form的类，便于下面调用"""
    class Meta:
        model = models.Role
        fields = ['title', ]

        # 调用bootCSS  给加上class=''即可  自定义样式！
        widgets = {
            'title': forms.TextInput(attrs={'class': 'layui-input'})
        }
