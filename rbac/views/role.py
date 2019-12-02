# create: '2018/12/13' - 362416272@qq.com  
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse  # 根据name反向生成url比较实用

from rbac.forms.role import RoleModelForm
from rbac import models


def role_list(request):
    """角色列表"""
    role_queryset = models.Role.objects.all()

    return render(request, 'rbac/role_list.html', {'roles': role_queryset})


def role_add(request):
    """添加角色"""
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))  # 根据
    else:
        # 如果提交空数据
        return render(request, 'rbac/change.html', {'form': form})


def role_edit(request, pk):
    """修改角色"""
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)  # instance=obj编辑页面带默认值
        return render(request, 'rbac/change.html', {'form': form, 'pk': pk})

    # POST
    form = RoleModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))  # 反向获取

    # 数据错误展示
    return render(request, 'rbac/change.html', {'form': form, 'pk': pk})


def role_del(request, pk):
    """删除角色"""
    origin_url = reverse('rbac:role_list')  # 反向取跳转链接
    if request.method == "GET":
        return render(request,'rbac/delete.html', {'cancel_url': origin_url})  # cancel_url是取消删除会跳地址

    # 确认删除
    models.Role.objects.filter(id=pk).delete()
    return redirect(origin_url)



