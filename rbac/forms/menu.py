# create: '2018/12/18' - 362416272@qq.com  
from django import forms
from django.utils.safestring import mark_safe
from rbac import models

from rbac.forms.base import BootStrapModelForm

icon_list = [
    ['fa fa-cab', mark_safe('<i class="fa fa-cab" aria-hidden="true"></i>')],  # mark_safe 等同于HTML中safe
    ['fa fa-credit-card-alt', mark_safe('<i class="fa fa-credit-card-alt" aria-hidden="true"></i>')],
    ['fa fa-bug', mark_safe('<i class="fa fa fa-bug" aria-hidden="true"></i>')],
    ['fa fa-cloud-download', mark_safe('<i class="fa fa fa-cloud-download" aria-hidden="true"></i>')],
    ['fa fa-cloud-upload', mark_safe('<i class="fa fa-cloud-upload" aria-hidden="true"></i>')],
    ['fa fa-clipboard', mark_safe('<i class="fa fa-clipboard" aria-hidden="true"></i>')],
    ['fa fa-cubes', mark_safe('<i class="fa fa-cubes" aria-hidden="true"></i>')],
    ['fa fa-film', mark_safe('<i class="fa fa-film" aria-hidden="true"></i>')],
    ['fa fa-hourglass-1', mark_safe('<i class="fa fa-hourglass-1" aria-hidden="true"></i>')],
    ['fa fa-navicon', mark_safe('<i class="fa fa-navicon" aria-hidden="true"></i>')],
    ['fa fa-pie-chart', mark_safe('<i class="fa fa-pie-chart" aria-hidden="true"></i>')],
    ['fa fa-rss', mark_safe('<i class="fa fa-rss" aria-hidden="true"></i>')],
    ['fa fa-reply-all', mark_safe('<i class="fa fa-reply-all" aria-hidden="true"></i>')],
    ['fa fa-clipboard', mark_safe('<i class="fa fa-clipboard" aria-hidden="true"></i>')],
    ['fa fa-unlock', mark_safe('<i class="fa fa-unlock" aria-hidden="true"></i>')],
    ['fa fa-user', mark_safe('<i class="fa fa-user" aria-hidden="true"></i>')],
    ['fa fa-video-camera', mark_safe('<i class="fa fa-video-camera" aria-hidden="true"></i>')],
    ['fa fa-wrench', mark_safe('<i class="fa fa-wrench" aria-hidden="true"></i>')],
    ['fa fa-trash-o', mark_safe('<i class="fa fa-trash-o" aria-hidden="true"></i>')],
]


class MenuModelForm(forms.ModelForm):
    """一级菜单FORM"""
    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
        # 给标签加上boot样式
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # 渲染的时候添加class属性
            'icon': forms.RadioSelect(  # 抓换成单选框 Radio
                choices=icon_list,
                attrs={'class': 'clearfix'}  # boot中清除浮动
            )
        }


class SecondMenuModelForm(BootStrapModelForm):  # 【继承事先写好的boot类直接实现添加boot样式】适用于简单的boot
    class Meta:
        model = models.Permission
        # fields = ['title', 'url', 'name', 'menu']
        exclude = ['pid']  # 等同于上面一行，只是排除掉pid不显示


class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'name', 'url']


class MultiAddPermissionForm(forms.Form):
    """批量添加"""
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


class MultiEditPermissionForm(forms.Form):
    """批量修改"""
    id = forms.IntegerField(
        widget=forms.HiddenInput()  # 自动隐藏
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')
