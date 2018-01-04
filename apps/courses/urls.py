
from django.conf.urls import url, include

from .views import (CourseListView, CourseDetailView, CourseStudyView, CourseCommentView,
                    CourseAddcommentView, CourseVideoView)


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),

    url(r'^study/(?P<course_id>\d+)/$', CourseStudyView.as_view(), name='study'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='comment'),
    url(r'^add_comment/$', CourseAddcommentView.as_view(), name='add_comment'),
    url(r'^video/(?P<video_id>.*?)/$', CourseVideoView.as_view(), name='video'),

]
