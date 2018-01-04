
from datetime import datetime

from django.db import models

from users.models import UserProfile


# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=32, verbose_name="城市名称")
    desc = models.CharField(max_length=256, verbose_name="城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=64, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    category_choices = (
        ('school', "高校"),
        ('person', "个人"),
        ('org', "培训机构"),
    )
    category = models.CharField(max_length=16, choices=category_choices, default='org', verbose_name="机构类别")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    images = models.ImageField(max_length=128, upload_to="org/%Y/%m", default="org/default.png", verbose_name="机构logo")
    students = models.IntegerField(default=0, verbose_name="学生人数")
    courses = models.IntegerField(default=0, verbose_name="课程数")
    address = models.CharField(max_length=128, verbose_name="机构地址")
    city = models.ForeignKey('CityDict', verbose_name="所在城市")
    tag = models.CharField(max_length=16, default="全国知名", verbose_name="机构标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_num(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(UserProfile, verbose_name="用户")
    org = models.ForeignKey('CourseOrg', verbose_name="所属机构")
    name = models.CharField(max_length=32, verbose_name="教师名称")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=64, verbose_name="就职公司")
    work_position = models.CharField(max_length=32, verbose_name="公司职位")
    points = models.CharField(max_length=64, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def get_courses(self):
        """ 获取某个老师的课程 """
        return self.course_set.all()

    def __str__(self):
        return self.name
