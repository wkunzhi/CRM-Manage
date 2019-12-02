# create: '2019/1/23' - 362416272@qq.com

import re

from collections import OrderedDict  # 有序字典
from django.conf import settings
from django.utils.module_loading import import_string  # 把字符串导入模块

from django.urls import URLResolver, URLPattern  # url文件中urlpatterns数组中,URLResolver=继续往下走还有分发，URLPattern=没有分发


def check_url_exclude(url):
    """定制~：自动收录路由，白名单"""
    # 通常情况下 admin这些路由不需要收录
    exclude_url = settings.AUTO_DISCOVER_EXCLUDE
    for regex in exclude_url:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归的去获取URL
    :param pre_namespace: namespace的别名前缀，以后用于拼接name 【namespace是分发的别名， name是路由的别名】
    :param pre_url:URL的地址前缀，以后用于拼接url
    :param urlpatterns:路由关系列表
    :param url_ordered_dict:用于保存递归获取到的所有路由
    :return:
    """
    for item in urlpatterns:
        route = ''
        # django2 后有了路由path 和 re_path更为方便，但两者的pattern不同（可以参考源码）所以要判断
        # 取当前层的路径route
        if item.pattern.__class__.__name__ == 'RoutePattern':  # 判断类名是不是RoutePattern
            route = item.pattern._route
        elif item.pattern.__class__.__name__ == 'RegexPattern':
            route = item.pattern._regex
        if isinstance(item, URLPattern):  # 没有分发,将路由添加到字典中
            if not item.name:
                continue  # 如果没有设置别名name就不管他，因为必须设置！！
            if pre_namespace:
                # 判断别名是否有前缀（不是一级分发） 比如'rbac:xxxx'
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + route  # pre_url是前缀，后面是当前项的url路径
            url = url.replace('^', '').replace('$', '')
            '''过滤掉白名单的，比如admin不需要收录'''
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}
        elif isinstance(item, URLResolver):
            # 还有分发，继续递归自己
            if pre_namespace:  # 如果有前缀，别名要拼接
                if item.namespace:  # 还要判断自身是否有namespace
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    # 如果自己没有namespace就用父级的
                    namespace = item.namespace
            else:
                if item.namespace:  # 如果自身有namespace，就用自身的
                    namespace = item.namespace
                else:
                    # 父级没有，自己也没有
                    namespace = None
            use_url = pre_url + route  # 上级的前缀url+ 自己的前缀
            recursion_urls(namespace, use_url, item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有URL(有序字典)【*********必须要给url设置别名Name且唯一*********】
    :return:
    """
    url_ordered_dict = OrderedDict()
    '''等同于 from luff.. import urls'''
    md = import_string(settings.ROOT_URLCONF)  # 取根路由路径（setting中配置的）,再以字符串形式导入包
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归获取所有路由，一级没有前缀所以=None 而且加上/
    return url_ordered_dict
