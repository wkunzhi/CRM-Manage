# 获取当前用户权限并存入session


from django.conf import settings  # 灵活配置


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user: 当前用户对象
    :param request: 请求相关所有数据
    :return:
    """
    # 取用户【权限+菜单信息】放入session。
    # __多对多跨表 _单跨表查询 distinct()去重 isnull==False不为空
    permission_queryset = current_user.roles.filter(permissions__isnull=False).order_by(
        'permissions__menu__sort').values("permissions__id",
                                          "permissions__url",
                                          "permissions__title",
                                          "permissions__name",
                                          "permissions__pid__id",
                                          "permissions__pid__title",
                                          "permissions__pid__url",
                                          "permissions__menu_id",
                                          "permissions__menu__icon",
                                          "permissions__menu__title",
                                          "permissions__menu__sort",
                                          ).distinct()
    # 取菜单+权限
    permission_dict = {}  # 储存权限信息（包含对应归属菜单 id，自己本身是菜单就为null）key 就是权限表中的别名name
    menu_dict = {}  # 储存（一二级）菜单信息 字典
    for item in permission_queryset:
        # 权限获取
        '''pid是权限所属于X菜单，在进入其权限url时，会默认选中归属的pid菜单'''
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid__id'],
            'p_title': item['permissions__pid__title'],  # 所属的菜单 名
            'p_url': item['permissions__pid__url']  # 所属的菜单 url
        }

        # 菜单获取（一二级菜单）
        menu_id = item['permissions__menu_id']  # id 为key
        if not menu_id:  # null则不是菜单
            continue

        node = {'id': item['permissions__id'], 'title': item['permissions__title'],
                'url': item['permissions__url']}  # 当前二级菜单信息存遍历node，便于调用
        if menu_id in menu_dict:
            # 有1级菜单id就添加append
            menu_dict[menu_id].get('children').append(node)
        else:
            # 没有1级菜单id就新建
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],  # 取menu表内对应一级菜单名
                'icon': item['permissions__menu__icon'],
                'sort': item['permissions__menu__sort'],
                'children': [node, ]
            }

    print('权限', permission_dict)
    print('菜单', menu_dict)
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
