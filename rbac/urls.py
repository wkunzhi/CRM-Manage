# create: '2018/12/13' - 362416272@qq.com  
from django.conf.urls import url
from django.urls import path
from rbac.views import role
from rbac.views import user
from rbac.views import menu

urlpatterns = [
    # 角色管理
    # 加上name可以让html动态反向获取url！！ 因为上级urls中有namespace=rbac语法{% url 'rbac:role_list' %}
    path('role/list/', role.role_list, name='role_list'),
    path('role/add/', role.role_add, name='role_add'),
    url(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),  # {% url 'rbac:role_edit' %}
    url(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),  # {% url 'rbac:role_edit' %}

    # 用户管理
    # path('user/list/', user.user_list, name='user_list'),
    # path('user/add/', user.user_add, name='user_add'),
    # url(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),  # {% url 'rbac:user_edit' %}
    # url(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),  # {% url 'rbac:user_edit' %}
    # url(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),  # {% url 'rbac:user_edit' %}


    # 权限分配菜单（一级菜单）
    path('menu/list/', menu.menu_list, name='menu_list'),
    path('menu/add/', menu.menu_add, name='menu_add'),
    url(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='menu_edit'),
    url(r'^menu/del/(?P<pk>\d+)/$', menu.menu_del, name='menu_del'),

    # 二级菜单
    url(r'^second/menu/add/(?P<menu_id>\d+)/$', menu.second_menu_add, name='second_menu_add'),
    url(r'^second/menu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    url(r'^second/menu/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),

    # 权限 三级菜单
    url(r'^permission/add/(?P<second_menu_id>\d+)/$', menu.permission_add, name='permission_add'),
    url(r'^permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name='permission_edit'),
    url(r'^permission/del/(?P<pk>\d+)/$', menu.permission_del, name='permission_del'),

    # 批量添加、编辑权限
    path('multi/permissions/', menu.multi_permissions, name='multi_permissions'),
    url(r'^multi/permissions/del/(?P<pk>\d+)/$', menu.multi_permissions_del, name='multi_permissions_del'),

    # 权限分配
    path('distribute/permissions/', menu.distribute_permissions, name='distribute_permissions'),
]
