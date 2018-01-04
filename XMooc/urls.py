"""XMooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView

import xadmin
from XMooc.settings import MEDIA_ROOT  # , STATIC_ROOT
from users.views import IndexView


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),    # 配置成 加载 xadmin
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', IndexView.as_view(), name='index'),

    # 配置验证码url
    url(r'^captcha/', include('captcha.urls')),

    # 配置 UEditor 富文本编辑器 url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    # 配置 处理media下面静态文件的url
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 配置 处理static下面静态文件的url
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # users的url配置放到了app目录下
    url(r'^users/', include('users.urls', namespace='user')),

    # orginazitiom的url配置放到了app目录下
    url(r'^org/', include('organization.urls', namespace='org')),

    # courses的url配置放到了app目录下
    url(r'^courses/', include('courses.urls', namespace='course')),

    # operation 的url配置放到了app目录下
    url(r'^operation/', include('operation.urls', namespace='operation')),

]

# 配置 403 404 500 页面
handler403 = 'users.views.page_not_allow'
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.server_error'
