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



# # 校区
# site.register(models.School, school.SchoolHandler)
# # 部门
# site.register(models.Department, depart.DepartHandler)
# # 用户
# site.register(models.UserInfo, userinfo.UserInfoHandler)
# # 课程
# site.register(models.Course, course.CourseHandler)
# # 班级
# site.register(models.ClassList, class_list.ClassListHandler)
# # 公户 设置url前缀 'pub'
# site.register(models.Customer, public_customer.PublicCustomerHandler, 'pub')
# # 私户 设置url前缀 'priv'
# site.register(models.Customer, private_customer.PrivateCustomerHandler, 'priv')
# # 跟进记录
# site.register(models.ConsultRecord, consult_record.ConsultRecordHandler)
# # 缴费记录
# site.register(models.PaymentRecord, payment_record.PaymentRecordHandler)
# # 财务审核
# site.register(models.PaymentRecord, check_payment_record.CheckPaymentRecordHandler, 'check')  # 重复了，所以加一个前缀
# # 学员
# site.register(models.Student, student.StudentHandler),
# # 积分管理
# site.register(models.ScoreRecord, score_record.ScoreHandler),
# # 上课管理
# site.register(models.CourseRecord, course_record.CourseRecordHandler),
