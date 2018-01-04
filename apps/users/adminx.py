
# __author__ = 'txowner'
# __time__ = '17-12-14 下午2:31'

import xadmin
from xadmin import views

from users.models import EmailVerifyRecord, Banner


# 设置这个类里面的两个变量为True(默认为False)， 用来开启主题功能(主题从google那边下载)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 这个用来 设置全局信息， 比如后台系统的标题， 页脚等。。。
class GlobalSetting(object):
    site_title = "XMooc 管理系统"     # 设置左上角的 标题
    site_footer = "XMooc 在线学习网"   # 设置页脚
    menu_style = 'accordion'   # 设置 注册的类的显示 折叠


class EmailVerifyRecordAdmin(object):
    """
    list_display : 后台进入当前app时，每条数据 显示哪些字段
    search_fields : 在当前表的搜索可以根据哪些字段值进行搜索（模糊匹配）
    list_filter : 在当前表中可以根据哪些字段进行过滤
    """
    list_display = ['email', 'code', 'send_type', 'send_time']
    search_fields = ['email', 'code', 'send_type']
    list_filter = ['email', 'code', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 注册 系统功能
# xadmin.site.register(views.BaseAdminView, BaseSetting) # 这个定制主题功能， 由于主要是从google请求过来， 所以一般国内没有用
xadmin.site.register(views.CommAdminView, GlobalSetting)

# 在后台系统中 注册 类
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)