
# 用来发送邮箱验证码
import random

from XMooc import settings
from django.core.mail import send_mail

from users.models import EmailVerifyRecord


HANDLE_DICT = {
    'register': {
        'subject': " XMooc 在线学习网注册激活邮件",
        'message': " 请点击以下链接完成账户激活：http://127.0.0.1:8000/users/active/{code}",
    },
    'forget': {
        'subject': " XMooc 在线学习网找回密码邮件",
        'message': " 请点击以下链接完成找回账户密码：http://127.0.0.1:8000/users/reset/{code}",
    },
    'update_email': {
        'subject': " XMooc 在线学习网修改用户邮箱邮件",
        'message': " 你的邮箱验证码是：{code}",
    }

}


def random_str(send_type):
    """
    用来生成 指定长度的 随机码
    :param code_length: 
    :return: 
    """
    source_str = settings.SOURCE_CODE_STR
    if send_type == 'update_email':
        code_length = 4
    else:
        code_length = settings.CODE_LENGTH

    code_str = ''
    for i in range(code_length):
        index = random.randint(0, len(source_str)-1)
        code_str += source_str[index]

    return code_str


def email_send(email, send_type='register'):
    """
    1、 生成一条数据，插入邮箱验证码表
    2、 向给定的email发一封相应的激活邮件
    :param email: 
    :param send_type: 
    :return: 
    """
    code = random_str(send_type)
    email_obj = EmailVerifyRecord()
    email_obj.email = email
    email_obj.code = code
    email_obj.send_type = send_type
    email_obj.save()

    status = send_mail(
        subject=HANDLE_DICT[send_type]['subject'],
        message=HANDLE_DICT[send_type]['message'].format(code=code),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
    return status

