"""
Django settings for XMooc project.

Generated by 'django-admin startproject' using Django 1.10.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')$9qpf04o#jri3n767q1#bvz!c7c6+w&9!x=0sz7vie1+y83wc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 指定 用户验证的类
AUTH_USER_MODEL = 'users.UserProfile'   # 注意，这里没有models， 不是完整的路径， 是 某个app 下面的 验证类

# 指定 验证用户登录的类(一般是用来扩展默认验证方法的功能，再覆盖)
AUTHENTICATION_BACKENDS = ['users.views.CustomBackends']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'courses',
    'organization',
    'operation',

    'xadmin',    # 这两个是安装 xadmin 需要注册的apps
    'crispy_forms',

    'captcha',  # 这个是用来配置 注册 图片验证码的
    'pure_pagination',  # 这个是 配置 分页功能的
    'DjangoUeditor',  #这个是 配置 UEditor 富文本编辑器
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'XMooc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates/users'),
            os.path.join(BASE_DIR, 'templates/organization'),
            os.path.join(BASE_DIR, 'templates/courses'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',   # 这里设置这个，就能直接在前段html中调用MEDIA_URLL
            ],
        },
    },
]

WSGI_APPLICATION = 'XMooc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "127.0.0.1",
        'NAME': "xmooc",
        'USER': "root",
        'PASSWORD': "root",
        'PORT': "3306",
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# LANGUAGE_CODE = 'en-us'  # 这个可以控制django 显示的语言，默认是英语
LANGUAGE_CODE = 'zh-hans'  # 这个在django1.8(不包括)以前是 zh-CN , 在1.8后改为了 zh-hans

# TIME_ZONE = 'UTC'   # 这个控制时区，一般改为上海
TIME_ZONE = 'Asia/Shanghai'   # 这个控制时区，一般改为上海

USE_I18N = True

USE_L10N = True

# USE_TZ = True  # 这个一般控制在数据库存储的时间， 为True时，是国际时间，一般改为False，表示使用本地时间
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# 静态文件一般是已经存在，程序要从给定路径去找， 所以一般是多个
"""
当 DEBUG=True 时， django遇到请求STATIC_URL的，就会到STATICFILES_DIRS指定的文件夹下面去找目标文件
当 DEBUG=False时， django就不会识别STATIC_URL，此时就需要像MEDIA_URL一样在url中配置
"""
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 当DEBUG为False时， 必须设置ALLOW_HOST, 切django不会自动去处理STATIC_URL的请求，需要像MEDIA_URL一样在url中配置
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# media 中存放的一般是上传的文件， 所以需要唯一指定一个上传地址
MEDIA_URL = '/media/'  # 上传文件时的url
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # 文件上传的具体文件夹(绝对路径)
# 在settings中 配置好这里时，后台上传就没问题了，要在前段页面中能访问到media中的文件， 还要在url.py中设置media的url


# 邮箱随机码 种子设置
SOURCE_CODE_STR = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsDdUuVvWwXxYyZz0123456789'
CODE_LENGTH = 16   # code 的长度

# 邮箱账号设置
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '46785647@qq.com'  # 你的 QQ 账号
EMAIL_HOST_PASSWORD = 'jzsxdbxbpjcmbjhd'
EMAIL_USE_TLS = True  # 这里必须是 True，否则发送不成功
# EMAIL_FROM = '46785647@qq.com'  # 你的 QQ 账号
DEFAULT_FROM_EMAIL = 'XMooc Designer <46785647@qq.com>'

# 配置分页方面的设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 6,  # 单边最大显示6页的页码
    'MARGIN_PAGES_DISPLAYED': 2,  # 相对的另一边显示2页的页码
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}
