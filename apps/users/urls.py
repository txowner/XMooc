
from django.conf.urls import url

from .views import (LoginView, LogoutView, RegisterView, ActiveView, ForgetpwdView, ResetpwdView, UserInfoView,
                    UpdateImageView, UpdatePasswdView, UpdateEmailView, UserInfoCourseView, UserInfoFavCoursesView,
                    UserInfoFavOrgsView, UserInfoFavTeachersView, UserInfoMessageView)


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetpwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetpwdView.as_view(), name='reset_pwd'),

    # 用户中心的url配置
    url(r'^info/$', UserInfoView.as_view(), name='info'),   # 用户信息页面显示或修改
    url(r'^image/upload/$', UpdateImageView.as_view(), name='update_image'),  # 更新用户头像
    url(r'^passwd/update/$', UpdatePasswdView.as_view(), name='passwd_update'),  # 更新用户密码
    url(r'^email/update/$', UpdateEmailView.as_view(), name='email_update'),  # 获取邮箱验证码以及更新用户邮箱

    url(r'^user_courses/$', UserInfoCourseView.as_view(), name='user_courses'),  # 获取我的课程
    url(r'^user_fav_courses/$', UserInfoFavCoursesView.as_view(), name='user_fav_courses'),  # 获取我收藏的课程
    url(r'^user_fav_orgs/$', UserInfoFavOrgsView.as_view(), name='user_fav_orgs'),  # 获取我收藏的课程机构
    url(r'^user_fav_teachers/$', UserInfoFavTeachersView.as_view(), name='user_fav_teachers'),  # 获取我收藏的老师

    url(r'^message/$', UserInfoMessageView.as_view(), name='message'),  # 加载用户消息
]
