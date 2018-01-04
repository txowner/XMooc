
from django.conf.urls import url, include
from .views import (OrglistView, OrghomeView, OrgcourseView, OrgdescView, OrgteacherView, TeacherListView,
                    TeacherDetailView)


urlpatterns = [
    url(r'^list/$', OrglistView.as_view(), name='list'),
    url(r'^home/(?P<org_id>\d+)/$', OrghomeView.as_view(), name='home'),
    url(r'^courses/(?P<org_id>\d+)/$', OrgcourseView.as_view(), name='courses'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgdescView.as_view(), name='desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgteacherView.as_view(), name='teacher'),

    # 配置teacher 相关页面
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]
