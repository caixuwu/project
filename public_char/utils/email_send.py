import sys
sys.setdefaultencoding('utf8')
from django.core.mail import send_mail
import random,datetime
from books.models import VerifyEmail
from HelloWorld.settings import EMAIL_FROM

#随机生成验证码的函数
def random_codestr(codelength=16):
    char = 'ABCDEFGHIJKLMNOPQRSTUVWSYZabcdefghijklmnopqrstuvwsyz0123456789'
    length = len(char)-1
    str = ''
    for i in range(codelength):
        str += char[random.randint(0,length)]
    return str


def send_email_to_user(email):
    #生成16位随机验证码
    code = random_codestr()
    #发送注册邮件
    mail_title = u"达摩院聊天室账号找回密码"
    mail_body = u"点击一下链接，重置你的密码：http://127.0.0.1:8888/forgetPwd/reset_pwd/%s"%code
    try:
        status = send_mail(mail_title, mail_body, EMAIL_FROM, [email])
    except Exception as e:
        return 0
    else:
        #发送成功
        if status == 1:
            email_record = VerifyEmail()
            email_record.code = code
            email_record.email = email
            time = datetime.timedelta(3)
            email_record.gq_time = datetime.datetime.now() +time
            email_record.save()
        return status


















