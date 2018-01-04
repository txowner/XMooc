from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course
# Create your models here.


class UserAsk(models.Model):
    """ 用户咨询 """
    name = models.CharField(max_length=32, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=64, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    """ 用户课程 """
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class CourseComment(models.Model):
    """ 课程评论 """
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    comments = models.CharField(max_length=256, default='', verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments


class UserFavorite(models.Model):
    """ 用户收藏 """
    user = models.ForeignKey(UserProfile, verbose_name="用户收藏")
    fav_id = models.IntegerField(default=0, verbose_name="数据ID")
    fav_type_choices = (
        (1, "课程"),
        (2, "课程机构"),
        (3, "讲师"),
    )
    fav_type = models.IntegerField(choices=fav_type_choices, default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    """ 用户消息 """
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=512, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


