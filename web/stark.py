# by 362416272@qq.com


from stark.service.v1 import site
from web import models
from web.views import company, userinfo, food, card


# 企业 - 列表
site.register(models.Company, company.CompanyHandler)

# 企业 - 资质
site.register(models.Card, card.CardHandler)

# 餐饮
site.register(models.Food, food.FoodHandler)

# 用户
site.register(models.UserInfo, userinfo.UserInfoHandler)

# 部门
# site.register(models.Department, depart.DepartHandler)
# 用户
# site.register(models.UserInfo, userinfo.UserInfoHandler)
