# create: '2018/12/10' - 362416272@qq.com  
from django.conf import settings
from django.template import Library
from collections import OrderedDict  # 排序dict
from rbac.service import urls

register = Library()  # 必须叫着名字

# 使用方法：
# 1. 在要引用的html中 {% load rbac(文件名) %}
# 2. 在引用地点 {% static_menu(函数名) request(传参过来) %}
# 优势
# 可插拔式


# 二级菜单使用方法
@ register.inclusion_tag('rbac/multi_menu.html')  # 告诉模板的路径，等待return传值渲染
def multi_menu(request):
    """
    自动创建二级菜单
    :return:
    """
    menu_dict = request.session[settings.MENU_SESSION_KEY]
    '''必须排序，因为dict 是无序的，可能后台显示菜单每次顺序不同'''
    # 对字典的key进行排序
    key_list = menu_dict
    # 空的有序字典
    ordered_dict = OrderedDict()

    '''思路：默认全部隐藏（class:hide）'''
    # 自动隐藏 + 选中状态
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'  # 默认情况所有都隐藏 hide

        # 如果字典中url跟当前url相等，那么class:hide换成active
        for per in val['children']:
            if per['id'] == request.current_selected:
                per['class'] = 'layui-this'  # 给自己（当前children）加一个class：active
                val['class'] = ''  # 父亲加上空（展开）
        ordered_dict[key] = val

    return {'menu_dict': ordered_dict}  # 将return的值，传给@的模板进行渲染


# 用户后台访问路径展示
@ register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'record_list': request.url_record}


# 在模板中可以直接调用，前提是先 {% load %}  用处就是在模板中调用后可以执行该方法
# 最多两个参数
# 语法{% if request|has_permission:'customer_add' %}  第一个参数放在前面| 第二个参数：''
#             {% endif %}
@ register.filter
def has_permission(request, name):
    """
    粒度控制：判断是否有权限
    :param request:
    :param name:
    :return:
    """
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True
    else:
        return False


# 功能：用户新建操作时跳转新页面会携带一组get参数，该参数会在新建页面新建完成跳转回之前页面的时候被解析回来
# 效果：跳转回来还是之前的状态
@register.simple_tag()
def memory_url(request, name, *args, **kwargs):  # *后面还可以传递本身就有的get参数
    """生产带有原条件的url【为了查看方便，该方法内容放在了rbac.service】直接调用该方法这里"""
    return urls.memory_url(request, name, *args, **kwargs)
