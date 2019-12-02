# create: '2018/12/13' - 362416272@qq.com
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse  # 根据name反向生成url比较实用

from rbac.forms.user import *
from rbac.models import UserInfo


def user_list(request):
    """用户列表"""
    user_queryset = UserInfo.objects.all()

    return render(request, 'rbac/user_list.html', {'users': user_queryset})


def user_add(request):
    """添加用户"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))  # 根据
    else:
        # 如果提交空数据
        return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    """修改用户"""
    obj = UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)  # instance=obj编辑页面带默认值
        return render(request, 'rbac/change.html', {'form': form, 'pk': pk})

    # POST
    form = UpdateUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))  # 反向获取

    # 数据错误展示
    return render(request, 'rbac/change.html', {'form': form, 'pk': pk})


def user_del(request, pk):
    """删除用户"""
    origin_url = reverse('rbac:user_list')  # 反向取跳转链接
    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': origin_url})  # cancel_url是取消删除会跳地址

    # 确认删除
    UserInfo.objects.filter(id=pk).delete()
    return redirect(origin_url)


def user_reset_pwd(request, pk):
    """重置密码"""
    obj = UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = ResetPasswordUserModelForm()
        return render(request, 'rbac/change.html', {'form': form, 'pk': pk})

    # POST
    form = ResetPasswordUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))  # 反向获取

    # 数据错误展示
    return render(request, 'rbac/change.html', {'form': form, 'pk': pk})




