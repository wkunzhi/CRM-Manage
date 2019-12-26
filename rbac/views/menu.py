# create: '2018/12/18' - 362416272@qq.com

from django.shortcuts import render, redirect, HttpResponse
from collections import OrderedDict  # 有序字典
from django.forms import formset_factory  # 批量form
from django.conf import settings
from django.utils.module_loading import import_string  # 字符串转成import 模块

from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm, MultiAddPermissionForm, \
    MultiEditPermissionForm
from rbac.service.urls import memory_reverse
from rbac.service.routes import get_all_url_dict


# from django.urls import reverse  # 根据name反向生成url比较实用


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.order_by('sort')
    menu_id = request.GET.get('mid')  # 这是str类型 用户选择的一级菜单
    second_sid = request.GET.get('sid')  # 用户选择的二级菜单，做选中状态
    # print('second_sid', second_sid)
    # print('menu_id', menu_id)

    # 判断用户是否伪造请求并处理2级菜单
    menu_exists = models.Menu.objects.filter(id=menu_id).exists()  # 判断这个id是否存在，在传给前端判断（双重保障判断）
    if not menu_exists:
        menu_id = None
    second_menus = ''
    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)

    # 判断用户是否伪造请求并处理权限表
    second_menu_exists = models.Permission.objects.filter(id=second_sid).exists()  # 判断这个id是否存在，在传给前端判断（双重保障判断）
    if not second_menu_exists:
        second_sid = None
    if second_sid:
        # 取权限
        permissions = models.Permission.objects.filter(pid_id=second_sid)
    else:
        permissions = []

    return render(
        request,
        'rbac/menu_list.html',
        {
            'menus': menus,
            'second_menus': second_menus,
            'mid': menu_id,
            'second_sid': second_sid,
            'permissions': permissions,
        }
    )


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))  # memory_reverse自己写的反解析

    # 如果提交空数据
    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    """
    编辑菜单
    :param request:
    :param pk:
    :return:
    """
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)  # instance=obj编辑页面带默认值
        return render(request, 'rbac/change.html', {'form': form, 'pk': pk})  # memory_reverse自己写的反解析

    # POST
    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    # 数据错误展示
    return render(request, 'rbac/change.html', {'form': form, 'pk': pk})


def menu_del(request, pk):
    """删除"""
    url = memory_reverse(request, 'rbac:menu_list')  # 反向取跳转链接
    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': url})  # cancel_url是取消删除会跳地址
    # 确认删除
    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单id（用于设置默认值）
    :return:
    """
    menu_object = models.Menu.objects.filter(id=menu_id).first()  # 取出默认选中对象

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_object})  # ModelForm的 initial参数指，给指定字段赋值默认
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))  # memory_reverse自己写的反解析

    # 如果提交空数据
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param pk: 当前要编辑的二级菜单
    :return:
    """
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=obj)  # instance=obj编辑页面带默认值
        return render(request, 'rbac/change.html', {'form': form, 'pk': pk})  # memory_reverse自己写的反解析

    # POST
    form = SecondMenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    # 数据错误展示
    return render(request, 'rbac/change.html', {'form': form, 'pk': pk})


def second_menu_del(request, pk):
    """删除"""
    url = memory_reverse(request, 'rbac:menu_list')  # 反向取跳转链接
    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': url})  # cancel_url是取消删除会跳地址
    # 确认删除
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def permission_add(request, second_menu_id):
    """
    添加权限（三级菜单）
    :param request:
    :param second_menu_id:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        # 先查看id是否存在
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()

        if not second_menu_object:
            return HttpResponse('二级菜单不存在！请重试')

        # form.instance 中包含用户提交的所有值,重新把 second_menu_object添加进去
        # 因为用户填表的时候没有填入pid所以手动跟进值
        form.instance.pid = second_menu_object

        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))  # memory_reverse自己写的反解析

    # 如果提交空数据
    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk:编辑的id
    :return:
    """
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = PermissionModelForm(instance=obj)  # instance=obj编辑页面带默认值
        return render(request, 'rbac/change.html', {'form': form, 'pk': pk})  # memory_reverse自己写的反解析

    # POST
    form = PermissionModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    # 数据错误展示
    return render(request, 'rbac/change.html', {'form': form, 'pk': pk})


def permission_del(request, pk):
    """删除"""
    url = memory_reverse(request, 'rbac:menu_list')  # 反向取跳转链接
    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': url})  # cancel_url是取消删除会跳地址
    # 确认删除
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def multi_permissions(request):
    """批量操作权限"""
    post_type = request.GET.get('type')
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)  # 创建formset类
    generate_formset = None
    update_formset = None
    # 用户提交区
    if request.method == 'POST' and post_type == 'generate':
        # 批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():  # 表单验证
            object_list = []
            # 先判断有没有唯一索引限制
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()  # 唯一字段判断
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:  # 没有错误就批量增加
                models.Permission.objects.bulk_create(object_list, batch_size=100)  # 批量增加语法bulk_create
        else:
            # 显示错误信息
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        # 批量更新
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):  # 循环总个数
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')  # 拿到修改页面的id
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()  # 数据库已有数据
                    # 反射
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()  # 检测唯一
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset

    # 展示区
    # 1. 取项目中所有URL
    """
    all_url_dict格式
    {
        rbac:role_list {'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        rbac:role_add {'name': 'rbac:role_add', 'url': '/rbac/role/add/'},
        ...
    }
    """
    all_url_dict = get_all_url_dict()
    router_name_set = set(all_url_dict.keys())  # 设为集合

    # 2. 取数据库中所有URL
    permission = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()  # 创建集合
    for row in permission:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])  # 放到集合里
    """
    permission_dict格式
    {
        rbac:role_list {'name': 'rbac:role_list','title':'角色列表', 'url': '/rbac/role/list/'....},
        ...
    }
    """
    print('项目中所有权限', router_name_set)
    print('数据库中已录入的', permission_name_set)
    # 判断代码中path中和数据库中是否相等（防止万一改到代码后出现bug）
    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致！'

    # 3. 拿到两个集合可以进行对比(集合语法)，参考 【总】权限分配思路.md

    # 3.1 计算出应该增加的name
    '''关于formset的使用可以参考 【https://gitee.com/Zok/formset】 代码库'''
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set  # 生成新的
        # 制作添加的 formset
        generate_formset = generate_formset_class(initial=[row_dict for name, row_dict in all_url_dict.items() if
                                                           name in generate_name_list])  # 列表生成式,把应该增加的放到initial中

    # 3.2 计算该删除的name
    delete_name_list = permission_name_set - router_name_set  # 删除多的
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]  # 列表生成式

    # 3.3 计算出该更新的name
    if not update_formset:
        update_name_list = permission_name_set & router_name_set  # 更新（&取交集）
        # 制作formset （必须要一个隐藏的id字段，才能编辑）在数据库permission中取，因为数据齐全有title，menu_id等
        update_formset = update_formset_class(initial=[row_dict for name, row_dict in permission_dict.items() if
                                                       name in update_name_list])  # 列表生成式,把应该增加的放到initial中

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'generate_formset': generate_formset,
            'delete_row_list': delete_row_list,
            'update_formset': update_formset,
        }
    )


def multi_permissions_del(request, pk):
    """批量页面的权限删除"""
    url = memory_reverse(request, 'rbac:multi_permissions')  # 反向取跳转链接
    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': url})  # cancel_url是取消删除会跳地址
    # 确认删除
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """
    # 取业务中的用户表(因为设计成了可插拔式)
    user_model_class = import_string(settings.RBAC_USER_MODEL_CLASS)

    user_id = request.GET.get('uid')  # 传递过来的选中user
    user_object = user_model_class.objects.filter(id=user_id).first()
    if not user_object:  # 传过来的id不存在
        user_id = None

    role_id = request.GET.get('rid')  # 取选中的id
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':  # 用户点击的更新角色的按钮
        role_id_list = request.POST.getlist('roles')
        # 用户和角色关系添加到第三章表（关系表）
        if not user_object:
            return HttpResponse('请先选择用户再分配角色')
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':  # 用户点击的更新权限的按钮
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请先选择角色再分配权限')
        role_object.permissions.set(permission_id_list)

    # 取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}  # 列表生成式  {1:None,2:None,3:None}

    # 获取当前用户所有权限
    # 如果选中角色，优先显示选中的角色拥有的权限
    # 如果没选角色，才显示用户的权限

    if role_object:  # 选中了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}
    elif user_object:  # 如果没选角色但选中了用户
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}  # 都构造成dict
    else:
        user_has_permissions_dict = {}

    all_user_list = user_model_class.objects.all()
    all_role_list = models.Role.objects.all()

    """
    需要效果
    [
        {
            id:1,
            title:'业务管理'
            children:[
                {id:1,title:'账单列表',children:[再套一个。。。]},
                {id:2,title:'客户列表'},
            ]
        },
    ]
    """
    # 权限分配板块需要一个三层循环 【需要这里组装数据，传给前端渲染】

    # 所有的一级菜单
    all_menu_list = models.Menu.objects.values('id', 'title')
    # 制作字典原因：频繁查找，字典查找速度大于列表查找！
    all_menu_dict = {}  # 字典和列表是同一个内存地址，连体双胞胎。。。
    for item in all_menu_list:
        item['children'] = []  # 留位放二级菜单
        all_menu_dict[item['id']] = item

    # 获取所有的二级菜单  # menu__isnull=False  menu选项不为空，说明他是二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    all_second_menu_dict = {}
    # 二级菜单挂在到一级
    for row in all_second_menu_list:
        row['children'] = []  # 留位放三级菜单
        all_second_menu_dict[row['id']] = row
        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # 获取三级菜单（不能做菜单的权限）menu为空，说明是3级菜单，且必须有2级菜单为父权限
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title',
                                                                                     'pid_id')  # pid是2级菜单id
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue  # 数据不合法
        all_second_menu_dict[pid]['children'].append(row)

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'user_id': user_id,
            'role_id': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'user_has_permissions_dict': user_has_permissions_dict,
        },
    )
