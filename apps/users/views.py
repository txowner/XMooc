import json

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetpwdForm, ResetpwdForm, UserImageForm, UserInfoForm
from utils.user_emails import email_send
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher

# Create your views here.


class CustomBackends(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django处理存在数据库中的密码是加密的，传递过来的密码是明文的，不能直接判断，要用这个函数来实现验证
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_user = UserProfile()
            email = request.POST.get('email')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'msg': "用户已注册", 'register_form': register_form})

            register_user.username = email
            register_user.email = email
            password = request.POST.get('password')
            # 由于 django是存储的加密后的密码， 所以这里要先对前段传递的密码进行加密，再存入数据库
            # django.contrib.auth.hashers 下的 make_password 实现了对密码的加密
            register_user.password = make_password(password)
            register_user.is_active = False   # 这里注册时设置未激活，后面给邮箱激活链接

            status = email_send(email=request.POST.get('email'), send_type='register')
            if status:
                register_user.save()  # 如果邮件发送成功，调用 model 的save 方法，把注册的账号保存到数据库
                return redirect(reverse('index'))
            else:
                return render(request, 'register.html', {'msg': "邮箱验证失败，请重试"})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):
    def get(self, request, active_code):
        email_record_objs = EmailVerifyRecord.objects.filter(code=active_code)  # 可能不唯一(几率很小) 所以不用get
        if email_record_objs:
            for email_record_obj in email_record_objs:
                # 对用户激活
                email = email_record_obj.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

                # 给用户发送欢迎消息
                message = "欢迎来到XMooc在线学习网，希望你能在接下来的日子学习到你想获得的知识"
                UserMessage.objects.create(user=user.id, message=message)

            return redirect(reverse('index'))
        else:
            return render(request, 'active_fail.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': "用户未激活", 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': "请输入正确的用户名或密码", 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    """
    用户退出登录
    """
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))   # reverse 可以把url的名字转换成实际的相对路径


class ForgetpwdView(View):
    def get(self, request):
        forget_form = ForgetpwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetpwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            users = UserProfile.objects.filter(email=email)
            # 原本email字段没有设置唯一，但注册时验证了，不存在才能注册，所以这里查询结果，若存在，那就只有一个
            if users:
                status = email_send(email=email, send_type='forget')
                if status:
                    return render(request, 'login.html', {'forget_form': forget_form})
                else:
                    return render(request, 'reset_pwd_msg.html', {'msg': "修改密码邮件发送失败，请重试"})
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': "账户不存在"})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetpwdView(View):
    def get(self, request, reset_code):
        reset_form = ResetpwdForm()

        email_record_objs = EmailVerifyRecord.objects.filter(code=reset_code)
        if email_record_objs:
            for email_record in email_record_objs:
                email = email_record.email
                return render(request, 'password_reset.html',
                              {'reset_form': reset_form, 'email': email, 'code': reset_code})
        else:
            return render(request, 'reset_pwd_msg.html', {'msg': "你请求的链接有误，请重试"})

    def post(self, request, reset_code):
        reset_form = ResetpwdForm(request.POST)
        email = request.POST.get('email')
        email_record_objs = EmailVerifyRecord.objects.filter(code=reset_code, email=email)
        # 可以防止修改邮箱，导致 任意邮箱密码修改 的漏洞
        if reset_form.is_valid() and email_record_objs:
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password1')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html',
                    {'reset_form': reset_form, 'email': email, 'code': reset_code, 'msg': "两次密码不一致"})
            users = UserProfile.objects.filter(email=email)
            for user in users:
                user.password = make_password(pwd2)
                user.save()
            return redirect(reverse('user:login'))

        else:
            return render(request, 'reset_pwd_msg.html', {'msg': "你的请求存在问题，请确认后重试"})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户中心 信息 显示 或修改
    """
    def get(self, request):
        """ 显示用户个人信息页面 """
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        """ 修改用户的 个人信息 """
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        # 注意这里的 instance 参数， 有则代表更新，没有就是创建
        if user_info_form.is_valid():
            user_info_form.save()
            status = {'code': 0, 'msg': '更新成功'}
        else:
            status = {'code': 1, 'msg': user_info_form.errors}
        return HttpResponse(content=json.dumps(status), content_type="application/json")


class UpdateImageView(LoginRequiredMixin, View):
    """
    更新 用户头像
    """
    def post(self, request):
        # 注意这里验证form时， 需要把request.POST 和 request.FILES 都传递过来
        user_image_form = UserImageForm(request.POST, request.FILES, instance=request.user)
        if user_image_form.is_valid():
            user_image_form.save()
            status = {'code': 0, 'msg': '更新成功'}
        else:
            status = {'code': 0, 'msg': '更新失败'}
        return HttpResponse(content=json.dumps(status), content_type="application/json")


class UpdatePasswdView(View):
    """
    在个人中心更改用户密码
    """
    def post(self, request):
        rest_pwd_form = ResetpwdForm(request.POST)
        if rest_pwd_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 != pwd2:
                status = {'code': 1, 'msg': '两次密码不一致'}
                return HttpResponse(content=json.dumps(status), content_type='application/json')
            request.user.password = make_password(pwd2)
            request.user.save()
            status = {'code': 0, 'msg': '修改密码成功'}
            return HttpResponse(content=json.dumps(status), content_type='application/json')
        else:
            return HttpResponse(content=json.dumps(rest_pwd_form.errors), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改用户邮箱： 1、获取邮箱验证码 2、修改用户邮箱
    """
    def get(self, request):
        """ 获取邮箱验证码 """
        email = request.GET.get('email', '')
        if email and not UserProfile.objects.filter(email=email):
            status = email_send(email=email, send_type='update_email')
            if status:
                status = {'code': 0, 'msg': '邮箱验证码发送成功'}
            else:
                status = {'code': 1, 'msg': '邮箱验证码发送失败'}
        else:
            status = {'code': 1, 'msg': '当前邮箱已经存在'}
        return HttpResponse(content=json.dumps(status), content_type='application/json')

    def post(self, request):
        """ 修改用户的邮箱 """
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        email_record_obj = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if email_record_obj:
            request.user.email = email
            request.user.save()
            status = {'code': 0, 'msg': '邮箱修改成功'}
        else:
            status = {'code': 1, 'msg': '请输入正确的邮箱或验证码'}
        return HttpResponse(content=json.dumps(status), content_type='application/json')


class UserInfoCourseView(View):
    """
    用户中心的  我的课程
    """
    def get(self, request):
        """ 返回用户中心 我的课程 """
        user_course_objs = UserCourse.objects.filter(user=request.user)
        all_courses = [user_course_obj.course for user_course_obj in user_course_objs]

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        courses = p.page(page)

        return render(request, 'usercenter-mycourse.html', {
            'courses': courses,
        })


class UserInfoFavCoursesView(View):
    """ 
    用户中心 我的收藏的课程
    """
    def get(self, request):
        """ 请求 收藏的课程数据 """
        # 获取当前用户收藏的所有课程收藏对象
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)

        # 取出这些对象的id， 对应的就是课程的id
        course_ids = [fav_course.fav_id for fav_course in fav_courses]

        all_courses = Course.objects.filter(id__in=course_ids)

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        courses = p.page(page)

        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
        })


class UserInfoFavOrgsView(View):
    """ 
    用户中心 我的收藏的课程机构
    """
    def get(self, request):
        """ 请求 收藏的课程机构 数据 """
        # 获取当前用户收藏的所有课程机构收藏对象
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)

        # 取出这些对象的id， 对应的就是课程机构的id
        org_ids = [fav_org.fav_id for fav_org in fav_orgs]

        all_orgs = CourseOrg.objects.filter(id__in=org_ids)

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        orgs = p.page(page)

        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,
        })


class UserInfoFavTeachersView(View):
    """ 
    用户中心 我的收藏的教师
    """
    def get(self, request):
        """ 请求 收藏的教师 数据 """
        # 获取当前用户收藏的所有教师对象
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)

        # 取出这些对象的id， 对应的就是教师的id
        teacher_ids = [fav_teacher.fav_id for fav_teacher in fav_teachers]

        all_teachers = Teacher.objects.filter(id__in=teacher_ids)

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        teachers = p.page(page)

        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
        })


class UserInfoMessageView(View):
    """
    个人中心 用户消息 包括删除操作
    """
    def get(self, request):
        # 若带有id参数，则删除这条消息
        del_id = request.GET.get('del_id', '')
        if del_id:
            # 删除操作时，先查询出来，再删除
            UserMessage.objects.filter(id=del_id).delete()

        # 获取该用户的所有消息 并返回
        all_messages = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')

        # 配置分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 5, request=request)
        # 参数： 备份也的对象集，每页显示个数， request， 分页后的对象(其中包含了对象集的一部分)
        messages = p.page(page)

        # 每次发送到页面后，该消息标记为已读
        for message in messages.object_list:
            if not message.has_read:
                message.has_read = True
                message.save()   # 注意保存啊。。。

        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })


class IndexView(View):
    """
    网站 首页 动态展示信息配置
    """
    def get(self, request):
        # 取5张 轮播图
        five_banners = Banner.objects.all().order_by('index')[:5]

        # 取3张课程 轮播图
        banner_courses = Course.objects.filter(is_banner=True)[:3]

        # 按点击数 获取普通课程 6个
        courses = Course.objects.filter(is_banner=False).order_by('click_nums')[:6]

        # 获取 15个课程机构
        orgs = CourseOrg.objects.all().order_by('click_nums')[:15]

        return render(request, 'index.html', {
            'five_banners': five_banners,
            'banner_courses': banner_courses,
            'courses': courses,
            'orgs': orgs
        })


###########################################
#  配置403 404 500 页面
###########################################
def page_not_allow(request):
    # 配置 403 页面
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response


def page_not_found(request):
    # 配置 404 页面
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def server_error(request):
    # 配置 500 页面
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response