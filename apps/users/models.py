
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 定义一个user类，继承AbstractUser类，作用是扩展AbstractUser类， 在settings中用AUTH_USER_MODEL指定为用户验证的类
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=64, default="coder", verbose_name="昵称")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    gender_choices = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    )
    gender = models.CharField(max_length=8, choices=gender_choices, default='other', verbose_name="性别")
    mobile = models.CharField(max_length=32, null=True, blank=True, verbose_name="电话")
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name="地址")
    image = models.ImageField(
        upload_to='head_image/%Y/%m', max_length=128,
        default='head_image/default.png', verbose_name="头像")
    # ImageField 在数据库中保存的是图片的路径地址，也是CharField， 所以也要设置最大长度

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def get_unread_message_num(self):
        """ 获取用户的未读消息 在每个页面都要用到 所以绑定到request.user去 """
        from operation.models import UserMessage
        # 把导入放在是让在用的时候才导入，避免放在文件开头，那样会导致包的循环引用
        unread_message_num = UserMessage.objects.filter(user=self.id, has_read=False).count()
        return unread_message_num

    def __str__(self):
        return self.username


# 由于 邮箱验证码 和首页轮播图功能单一， 所以为了简便， 放在了users app 中
class EmailVerifyRecord(models.Model):
    email = models.EmailField(max_length=64, verbose_name="邮箱")
    code = models.CharField(max_length=32, verbose_name="邮箱验证码")
    send_type_choices = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '找回密码'),
    )
    send_type = models.CharField(choices=send_type_choices, max_length=16, verbose_name="类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email
    #     return "{code}({email})".format(code=self.code, email=self.email)
        # 这里 是设置在后台显示哪些字段信息，不重载_str_， 默认是当前类的对象
        # 这里设置 跟 admin中注册时，list_display显示是一样的，不过list_display效果更好，一般设置那个，但是档有外键时，就需要设置了


class Banner(models.Model):
    title = models.CharField(max_length=256, verbose_name="标题")
    image = models.ImageField(max_length=128, upload_to='banner/%Y/%m', verbose_name="轮播图")
    url = models.URLField(max_length=256, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="播放顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
