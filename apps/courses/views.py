import json

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, Video
from operation.models import UserCourse, UserFavorite, CourseComment, UserMessage
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    """
    课程列表页信息
    """
    def get(self, request):
        # 默认按照最新的排列
        all_courses = Course.objects.all().order_by('-add_time')

        # 搜索功能实现
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords) |
                Q(detail__icontains=keywords) | Q(tags__icontains=keywords)
            )

        # 热门课程推荐
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 展昭指定的方式对queryset进行排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            # 按照 热度 排列
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')

        # 实现分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
        })


class CourseDetailView(View):
    """
    课程详情页面
    """
    def get(self, request, course_id):
        # 找出这门课程
        course = Course.objects.get(id=int(course_id))

        # 每次请求一次这个页面， 课程的点击数 +1
        course.click_nums += 1
        course.save()

        # 找出学习这门课程的学生记录（取几个就是）
        user_courses = UserCourse.objects.filter(course=course)[:5]

        # 这个课程的所属机构
        course_org = course.course_org

        # 检查用户是否收藏该课程或则该机构
        fav_course = False
        fav_org = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user)
            if user_fav.filter(fav_type=1, fav_id=course.id):
                fav_course = True
            if user_fav.filter(fav_type=2, fav_id=course_org.id):
                fav_org = True

        # 课程相关推荐
        if course.tags:
            relate_courses = Course.objects.filter(tags=course.tags).order_by('-click_nums')[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            'user_courses': user_courses,
            'course_org': course_org,
            'fav_course': fav_course,
            'fav_org': fav_org,
            'relate_courses': relate_courses,

        })


class CourseStudyView(LoginRequiredMixin, View):
    """
    课程 学习 页面 信息
    """
    def get(self, request, course_id):
        # 找出这门课程
        course = Course.objects.get(id=int(course_id))

        # 每次点击开始学习， 这门课程的学习人数+1
        course.students += 1
        course.save()

        # 把 课程 与 用户绑定
        user_couses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_couses:
            UserCourse.objects.create(user=request.user, course=course)

            # 给用户发消息
            message = "欢迎学习{course_name}， 希望你能学有所获".format(course_name=course.name)
            UserMessage.objects.create(user=request.user.id, message=message)

        # 课程相关推荐
        if course.tags:
            relate_courses = Course.objects.filter(tags=course.tags).exclude(id=course.id).order_by('-click_nums')[:3]
        else:
            relate_courses = []

        return render(request, 'course-video.html', {
            'course': course,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程 评论 页面 信息
    """
    def get(self, request, course_id):
        # 找出这门课程
        course = Course.objects.get(id=int(course_id))

        # 查找学过该课程的同学 学的其他课程
        # user_ids = [user_course.user.id for user_course in course.usercourse_set.all()]
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]

        all_users_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_users_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:3]
        # if course.tags:
        #     relate_courses = Course.objects.filter(tags=course.tags).exclude(id=course.id).order_by('-click_nums')[:3]
        # else:
        #     relate_courses = []

        return render(request, 'course-comment.html', {
            'course': course,
            'relate_courses': relate_courses,
        })


class CourseVideoView(LoginRequiredMixin, View):
    """
    播放 视频
    """
    def get(self, request, video_id):
        # 找到这个视频
        video = Video.objects.get(id=int(video_id))

        # 找出这门课程
        course = video.lesson.course

        # 课程相关推荐
        if course.tags:
            relate_courses = Course.objects.filter(tags=course.tags).exclude(id=course.id).order_by('-click_nums')[:3]
        else:
            relate_courses = []

        return render(request, 'play-video.html', {
            'video': video,
            'course': course,
            'relate_courses': relate_courses,
        })


class CourseAddcommentView(View):
    """
    添加评论
    """
    def post(self, request):
        course_id = request.POST.get('course_id', '')
        comments = request.POST.get('comments', '')

        # 只有登陆后才能收藏
        if not request.user.is_authenticated():
            status = {'code': 1, 'msg': '用户未登录'}
            return HttpResponse(content=json.dumps(status), content_type='application/json')

        if course_id and comments:
            CourseComment.objects.create(user=request.user, course_id=course_id, comments=comments)
            status = {'code': 0, 'msg': '评论成功'}
        else:
            status = {'code': 1, 'msg': '评论失败'}

        return HttpResponse(content=json.dumps(status), content_type='application/json')

