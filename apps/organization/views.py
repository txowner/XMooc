
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import CityDict, CourseOrg, Teacher
from operation.models import UserFavorite

# Create your views here.


class OrglistView(View):
    """
    有关 机构的 相关视图
    """
    def get(self, request):
        # 查询所有的城市信息
        all_citys = CityDict.objects.all()

        # 查询所有的机构信息
        all_orgs = CourseOrg.objects.all()

        # 搜索功能实现
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 根据城市， 做进一步的筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 根据类别， 做进一步的筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据类别， 做进一步的筛选
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-courses')

        # 对查询出来的结果的个数进行计数
        org_num = all_orgs.count()

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_citys': all_citys,
            'orgs': orgs,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'sort': sort,
            'hot_orgs': hot_orgs,
        })


class OrghomeView(View):
    """ 机构首页信息 """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)

        # 每次点击机构的home页， 其点击数+1
        course_org.click_nums += 1
        course_org.save()

        # 机构的全部课程
        all_courses = course_org.course_set.all()

        # 机构的老师
        all_teachers = course_org.teacher_set.all()

        # 检查用户是否收藏该机构
        fav_org = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user)
            if user_fav.filter(fav_type=2, fav_id=course_org.id):
                fav_org = True

        return render(request, 'org-detail-homepage.html',{
            'course_org': course_org,
            'courses': all_courses[:3],
            'teachers': all_teachers[:2],
            'fav_org': fav_org,
        })


class OrgcourseView(View):
    """ 机构课程信息 """
    def get(self, request, org_id):
        current_page = "courses"
        course_org = CourseOrg.objects.get(id=org_id)
        # 机构的全部课程
        all_courses = course_org.course_set.all()

        # 检查用户是否收藏该机构
        fav_org = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user)
            if user_fav.filter(fav_type=2, fav_id=course_org.id):
                fav_org = True

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 8, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            'current_page': current_page,
            'course_org': course_org,
            'courses': courses,
            'fav_org': fav_org,
        })


class OrgdescView(View):
    """ 机构介绍 """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=org_id)

        # 检查用户是否收藏该机构
        fav_org = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user)
            if user_fav.filter(fav_type=2, fav_id=course_org.id):
                fav_org = True

        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org,
            'fav_org': fav_org,
        })


class OrgteacherView(View):
    """ 机构教师信息 """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=org_id)

        # 机构的老师
        all_teachers = course_org.teacher_set.all()

        # 检查用户是否收藏该机构
        fav_org = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user)
            if user_fav.filter(fav_type=2, fav_id=course_org.id):
                fav_org = True

        return render(request, 'org-detail-teachers.html', {
            'current_page': current_page,
            'course_org': course_org,
            'teachers': all_teachers,
            'fav_org': fav_org,
        })


class TeacherListView(View):
    """
    用户列表信息
    """
    def get(self, request):
        # 查询所有的老师
        all_teachers = Teacher.objects.all()

        # 搜索功能实现
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=keywords) | Q(work_company__icontains=keywords) |
                Q(work_position__icontains=keywords) | Q(work_company__icontains=keywords)
            )

        # 所有老师的个数
        teachers_nums = all_teachers.count()

        # 排序功能
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        # 讲师排行榜
        sorted_teachers = all_teachers.order_by('-click_nums')[:3]

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 2, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'teachers_nums': teachers_nums,
            'teachers': teachers,
            'sort': sort,
            'sorted_teachers': sorted_teachers,
        })


class TeacherDetailView(View):
    """
    教师详情页面
    """
    def get(self, request, teacher_id):
        # 获取这个老师
        teacher = Teacher.objects.get(id=int(teacher_id))

        # 每次访问某个讲师详情页，他的点击数 +1
        teacher.click_nums += 1
        teacher.save()

        # 查询他的全部课程
        all_courses = teacher.course_set.all()

        # 讲师排行榜
        sorted_teachers = Teacher.objects.order_by('-click_nums')[:3]

        # 检查用户是否收藏该教师或则机构
        fav_teacher = False
        fav_org = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user)
            if user_fav.filter(fav_type=3, fav_id=teacher.id):
                fav_teacher = True
            if user_fav.filter(fav_type=2, fav_id=teacher.org.id):
                fav_org = True

        # 配置课程的分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 1, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        courses = p.page(page)

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'sorted_teachers': sorted_teachers,
            'fav_teacher': fav_teacher,
            'fav_org': fav_org,
        })
