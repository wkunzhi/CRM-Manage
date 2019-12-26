# 中间件 在每次访问页面时 验证该页面是否能访问
# -*- coding:utf-8 -*-
import re
from django.utils.deprecation import MiddlewareMixin  # 中间件必须继承这
from django.shortcuts import HttpResponse
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        :param request:
        :return:
        """
        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        current_url = request.path_info

        # 白名单校验
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:  # 0权限，没有登录
            return HttpResponse('未获取到用户权限信息，请登录！<a href="login">点击登录</a>')

        # 非菜单的权限链接处理
        url_record = [
            {'title': '首页', 'url': '#'}
        ]

        # 此处判断： 如果是 /logout/ /index/ 这种登录成功，但是不需要校验权限的页面
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                request.current_selected = 0  # 默认展开菜单
                request.url_record = url_record
                # 需要登录当时无需权限的页面直接通过
                return None

        flag = False

        # 权限含有正则，so要用正则匹配权限
        # for i in permission_dict.values():
        #     print(i)
        for item in permission_dict.values():
            # print(item.regex.search(item.get('url')))
            reg = "^%s$" % item.get('url')  # 必须加上起始 终止符！！
            if re.match(reg, current_url):
                flag = True
                # 获取pid归属母菜单，没有就取id说明自身就是菜单（再根据id交给inclusion_tag，渲染选中母菜单）!!
                request.current_selected = item['pid'] or item['id']  # 如果pid为null就 or后面的值

                # 非菜单的权限链接 做归属 (给最后一个加'class': 'active'因为路径最后一层为当前，所以不可选)
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])

                request.url_record = url_record  # 开一个变量，存储访问路径结构，网页需要的时候直接调用
                break

        if not flag:
            return HttpResponse('你的账户无权访问该页面<a href="/login">点击登录</a>')
