
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=64, verbose_name="课程名称")
    desc = models.CharField(max_length=256, verbose_name="课程描述")
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构")
    teacher = models.ForeignKey(Teacher, verbose_name="教师")
    # detail = models.TextField(verbose_name="课程详情")
    detail = UEditorField(width=600, height=300, imagePath="courses/ueditor/images/",
                    filePath="courses/ueditor/files/", default='', verbose_name="课程详情")
    degree_choices = (
        ('simple', '初级'),
        ('middle', '中级'),
        ('high', '高级'),
    )
    degree = models.CharField(max_length=16, choices=degree_choices, default='middle', verbose_name="课程难度")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(max_length=128, upload_to='courses/%Y/%m', null=True, blank=True, verbose_name="封面图")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    tags = models.CharField(max_length=64, default='', verbose_name="课程类别")
    course_info = models.CharField(max_length=128, default='', verbose_name="课程须知")
    course_harvest = models.CharField(max_length=128, default='', verbose_name="课程收获")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_lesson_num(self):
        """ 获取课程的章节数 """
        return self.lesson_set.all().count()

    def get_all_lesson(self):
        """ 获取课程的所有章节 """
        return self.lesson_set.all()

    def get_course_resource(self):
        """ 获取课程的所有资源 """
        return self.courseresource_set.all()

    def get_course_comment(self):
        """ 获取课程的评论 """
        return self.coursecomment_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey('Course', verbose_name="课程")
    name = models.CharField(max_length=128, verbose_name="章节名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_all_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey('Lesson', verbose_name="章节")
    name = models.CharField(max_length=128, verbose_name="视频名称")
    url = models.CharField(max_length=256, default='', verbose_name="url地址")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey('Course', verbose_name="课程")
    name = models.CharField(max_length=128, verbose_name="资料名称")
    download = models.FileField(max_length=128, upload_to='courses/resource/%Y/%m', verbose_name="下载")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
