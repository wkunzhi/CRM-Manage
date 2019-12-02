# create: '2019/1/18' - 362416272@qq.com
from django.urls import reverse
from django.http import QueryDict  # 转义 会把等于号转为"%3D"


def memory_url(request, name, *args, **kwargs):  # *后面还可以传递本身就有的get参数
    """
    生产带有原条件的url
    :param request:
    :param name:
    :return:
    """
    basic_url = reverse(name, args=args, kwargs=kwargs)  # 反向生成args指，原搜索条件带进去
    if not request.GET:
        return basic_url
    else:
        old = request.GET.urlencode()  # 取 所有参数 ？号后面的
        # 加上前缀 比如？_filter+old 将参数打包 注意old必须要带上引号【转义】

        query_dict = QueryDict(mutable=True)
        query_dict['_filter'] = request.GET.urlencode()  # 这个类自动打包转义（之前的所有get参数）

        return "%s?%s" % (basic_url, query_dict.urlencode())


def memory_reverse(request, name, *args, **kwargs):
    """
    反向生成URL【把原来的urlGET参数获取并生成在新页面】
        例如：  /rbac/menu/add?_filter=mid%3D2
        1. 在url总将原来的搜索条件，如_filter后的值
        2. reverse生成原来的URL， 如 /menu/list/
        3. /menu/list/?mid=%3D2
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')  # 取参数
    if origin_params:  # 如果有原始的get参数
        url = '%s?%s' % (url, origin_params)
    return url
