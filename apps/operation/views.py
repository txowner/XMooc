import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from operation.models import UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher
from .models import UserFavorite
from .forms import UserAskForm

# Create your views here.


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask_obj = userask_form.save(commit=True)  # commit控制是否存储到数据库，默认为True，存储到数据库
            # 这里返回的 user_ask_obj 是UserAskForm对于的model UserAsk的实例

            status = {'code': 0, 'msg': '添加成功'}
        else:
            status = {'code': 1, 'msg': '添加失败'}

        return HttpResponse(content=json.dumps(status), content_type='application/json')


class FavView(View):
    """
    未收藏则点击收藏，若已收藏再点击就取消收藏
    """
    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        # 只有登陆后才能收藏
        if not request.user.is_authenticated():
            status = {'code': 1, 'msg': '用户未登录'}
            return HttpResponse(content=json.dumps(status), content_type='application/json')

        if fav_id > 0 and fav_type in (1, 2, 3):
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            # 这里查询看看，是否存在，存在就删除(取消收藏)，不存在就添加
            if user_fav:
                user_fav.delete()

                # 用户取消收藏后， 课程/课程机构/讲师 对应的收藏数-1
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num -= 1
                    if course.fav_num < 0:
                        course.fav_num = 0
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    if course_org.fav_nums < 0:
                        course_org.fav_nums = 0
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()

                status = {'code': 0, 'msg': '收藏'}
            else:
                UserFavorite.objects.create(user=request.user, fav_id=fav_id, fav_type=fav_type)

                # 用户收藏后， 课程/课程机构/讲师 对应的收藏数+1
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num += 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums += 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()

                # 给用户发送欢迎消息
                msg_list = ['', '']
                if fav_type == 1:
                    msg_list = ['课程', Course.objects.get(id=fav_id)]
                elif fav_type == 2:
                    msg_list = ['课程机构', CourseOrg.objects.get(id=fav_id)]
                elif fav_type == 3:
                    msg_list = ['讲师', Teacher.objects.get(id=fav_id)]

                message = "亲，你收藏了{type} {name}， 可以在我的收藏里面去查看详细信息哦".format(
                    type=msg_list[0], name=msg_list[1]
                )
                UserMessage.objects.create(user=request.user.id, message=message)

                status = {'code': 0, 'msg': '已收藏'}
        else:
            status = {'code': 1, 'msg': '收藏失败'}

        return HttpResponse(content=json.dumps(status), content_type='application/json')