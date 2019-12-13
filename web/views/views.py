from django.shortcuts import render, redirect

from rbac.service.init_permission import init_permission
from web import models as web
from web.utils.MD5 import gen_md5


def login(request):
    """
    登录
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    # 提交的登陆post
    user = request.POST.get('user')
    pwd = gen_md5(request.POST.get('pwd', ''))
    # 进行账号认证
    user = web.UserInfo.objects.filter(name=user, password=pwd).first()
    if not user:  # 有这个用户
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    init_permission(user, request)  # 权限初始化
    request.session['user_info'] = {'id': user.id, 'nickname': user.nickname}
    # return JsonResponse({'user': "OK"})
    return redirect('/rbac/menu/list/')


def logout(request):
    """
    退出
    :param request:
    :return:
    """
    request.session.delete()

    return redirect('/login/')


def index(request):
    return render(request, 'index.html')


