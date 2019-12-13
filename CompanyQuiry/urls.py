from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from web.views import views
from stark.service.v1 import site

urlpatterns = [
    path('admin/', admin.site.urls),

    # 路由系统
    url(r'^stark/', site.urls),
    # 权限系统
    url(r'^rbac/', include(('rbac.urls', 'rbac'), namespace='rbac')),


    # 用户
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^index/', views.index, name='index'),
    url(r'^$', views.login, name='login'),
]
