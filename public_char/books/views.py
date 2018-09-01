from django.shortcuts import render, redirect
# from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from books import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate  # 密码验证函数
from django.contrib import auth
# from django.views.decorators.csrf import csrf_protect#发生403错误时增加
import json
import queue
import time
from .forms import RegisterForm
from PIL import Image  # 形成图像缩略图
from django.views import View
from books import forms
from utils.email_send import *

MSG_QUEUES = {}
class Reset_pwd(View):
    def get(self,request,reset_code):
        forget_form = forms.ForgetPasswordForm()
        email_yan_zheng = models.VerifyEmail.objects.filter(code=reset_code)
        if email_yan_zheng:
            email_recode = models.VerifyEmail.objects.get(code=reset_code)
            if email_recode.is_use == 'no':
                now_time = datetime.datetime.now()
                now_time = now_time.strftime('%Y%m%d %H%M%S')
                gq_time = email_recode.gq_time.strftime('%Y%m%d %H%M%S')
                if now_time<=gq_time:
                    email_recode.is_user = 'yes'
                    email_recode.save()
                    return render(request,'reset_pwd.html',{'email':email_recode.email,'forget_form':forget_form})
                else:
                    return HttpResponse('此忘记密码的激活已过期，<a href="/forget/">请进入忘记密码页面，重新发送重置邮件</a>')
            else:
                return HttpResponse('该激活邮件已被使用，<a href="/forget/">请进入忘记密码页面，重新发送重置邮件</a>')
        else:
            return render(request,'forgetpwd.html')


class ForgetPassword(View):
    def get(self,request):
        forget_form = forms.ForgetPasswordForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = forms.ForgetPasswordForm(request.POST)
        if forget_form.is_valid():
            uemail = request.POST.get('email', '')
            user_email = models.Email.objects.filter(email=uemail)
            if user_email:
                status = send_email_to_user(uemail)
                if status:
                    return render(request,'send_success.html',{'email':uemail})
                else:
                    forget_form = forms.ForgetPasswordForm()
                    return render(request, 'forgetpwd.html', {'msg':'该邮箱不存在', 'forget_form':forget_form})
            else:
                return render(request,'forgetpwd.html',{'forget_form':forget_form})

class Modify_pwd(View):
    def post(self,request):
        uemail = request.POST.get('email','')
        modify_form = forms.Modify_pwdForm(request.POST)
        if modify_form.is_valid():
            password = request.POST.get('password','')
            r_password = request.POST.get('r_password','')
            if password == r_password:
                try:
                    user = models.Email.objects.get(email=uemail)
                    user.passwd = make_password(password)
                    user.save()
                    return HttpResponse('密码重置成功，<a href="/dmy.html/">请点击登录</a>')
                except Exception as e:
                    return HttpResponse('不存在此用户，<a href="/register.html/">请点击注册</a>')
            else:
                return render(request,'reset_pwd.html',{'msg':'两次密码输入不一致，请重新输入','modify_form':modify_form,'email':uemail})
        else:
            return render(request, 'reset_pwd.html',{'msg': '两次密码输入不一致，请重新输入', 'modify_form': modify_form, 'email': uemail})






def dmy(request):
    if request.method == 'GET':
        return render(request, 'dmy.html')
    elif request.method == 'POST':
        nm = request.POST.get('name', '')
        pwd = request.POST.get('passwd', '')

        # try:
        if nm:
            data = models.User.objects.filter(name=nm)
            if data:
                result = check_password(pwd, data[0].passwd)
                print(result)
                if result :

                    request.session['is_hero'] = True
            # request.session.setdefault('k1',123)  存在则不设置
                    request.session['user'] = nm
                    return redirect('/index.html/')
                else:
                    passwd_error='密码错误'
                    print('--->')
                    return render(request, 'dmy.html',{'passwd_error':passwd_error})
            else:
                name_error='用户名不存在'
                return render(request, 'dmy.html',{'name_error':name_error})

        # result = authenticate(name=nm, password=pwd)

        else:
            return render(request, 'dmy.html')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        # return render_to_response('register.html',locals())
    elif request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        # form_image=RegisterForm(request.FILES)
        # print('-->',form_image)
        errors = {}
        if form.is_valid():
            data = form.cleaned_data
            data.pop('passwd_again')
            print(len(make_password(data['passwd'])))
            data['passwd'] = make_password(data['passwd'])
            print(data)
            models.User.objects.create(**data)
            # data=models.User.objects.create()
            return redirect('/dmy.html/')
        else:
            errors = form.errors
    return render(request, 'register.html', locals())


def index(request):

    #     #cookie做法
    #     # if request.COOKIES.get('username',None):
    #     #     name=request.COOKIES.get('username',None)
    #     #     return render_to_response('index.html',locals())
    if request.session.get('is_hero', None):
        my_name = request.session.get('user', None)
        
        data = models.User.objects.get(name=my_name)
        my_head = data.head_img
        
        my_id = data.id
        my_signature = data.signature
        print('--->>>>', my_head)

        if my_head:
            reqimage = Image.open(my_head)
            reqimage.thumbnail((128, 128), Image.ANTIALIAS)
            print('-->', reqimage)

        # q = models.UserInfo.objects.all()
        # .values('name','id','ut__title').filter(id__lt=60)
        #q = models.UserInfo.objects.all().select_related('ut').filter(id__lt=60)
        # select_related('ut') 相当 于 inner join 先连成一张表再进行查询
        friends_list = models.User.objects.all()
        group_list = models.WebGroup.objects.all()
        return render(request, 'chat_main.html', locals())
    else:
        return redirect('/dmy.html/')

# 用类写,get方法就是get,post方法就是post
# from django.views.generic.base import View

# class Cbv(View):
#     def dispatc(self,request,*args,**kwargs):
#         #不管get还是post都要经过这里,可以定制
#         result=super(Cbv,self).dispatc(self,request,*args,**kwargs)
#         return result
#     def get(self,request):
#         return HttpResponse('Cbv.get')

#     def post(self,request):
#         ret= HttpResponse('Cbv.post')#这里就是响应体
#         ret['h1']='v1'#这就是响应头(django要求这样写的)
#         return ret


def send_msg(request):
    my_name = request.session.get('user', None)
    my_id = models.User.objects.get(name=my_name).id
    print(request.POST)
    msg_data = request.POST.get('data')
    if msg_data:
        msg_data = json.loads(msg_data)
# 没有导入json模块时,前端出现jquery模块query-3.3.1.js:9600; 500 (INTERNAL SERVER ERROR)
        msg_data['timestamp'] = time.time()
        if msg_data['type'] == 'single':
            sdata = int(msg_data['to'])
            if not MSG_QUEUES.get(sdata):
                MSG_QUEUES[sdata] = queue.Queue()
            MSG_QUEUES[sdata].put(msg_data)
        else:

            # 群聊,找到该组的所有成员
            group_obj = models.WebGroup.objects.get(id=int(msg_data['to']))
            # 往下是添加字段到members,目前是只要进行群聊就加进去了

            user_obj = models.User.objects.get(id=my_id)
            group_obj.members.add(user_obj)
            group_obj.save()
            # print(group_obj.members.all())
            for member in group_obj.members.select_related():
                # prefetch_related()和select_related()的

                # 这里查询的结果是User里的所有字段还是只有Id(会不会浪费?)
                print('member:', member)
                if not MSG_QUEUES.get(member.id):
                    MSG_QUEUES[member.id] = queue.Queue()
                if member.id != my_id:
                    MSG_QUEUES[member.id].put(msg_data)
        print('send_msg', MSG_QUEUES)

    return HttpResponse("---msg recevied---")


def get_msg(request):
    print('get_msg')
    # 用以下两个必须在admin里面注册
    # my_id=request.user.id
    # my_name=request.user

    my_name = request.session.get('user', None)
    my_id = models.User.objects.get(name=my_name).id
    print(my_name, my_id)
    # 判断自己有没有queue,如果新用户第一次登录就是没有queue
    if my_id not in MSG_QUEUES:
        print('no queue for user[%s]' % my_id, my_name)
        # 创建一个queue
        MSG_QUEUES[my_id] = queue.Queue()
    # 获取消息的大小
    msg_count = MSG_QUEUES[my_id].qsize()
    q_obj = MSG_QUEUES[my_id]
    msg_list = []
    if msg_count > 0:
        for msg in range(msg_count):
            msg_list.append(q_obj.get())
        print('new msgs:', msg_list)
    else:
        print('get', MSG_QUEUES)
        try:
            msg_list.append(q_obj.get(timeout=30))
        except queue.Empty:
            print('\033[41m;no msg\033[0m')

    return HttpResponse(json.dumps(msg_list))


def file_upload(request):
    print('file:', request.FILES)
    file_obj = request.FILES.get('file')
    new_file_name = 'uploads/%s' % file_obj.name
    with open(new_file_name, 'wb+') as new_fo:
        for chunk in file_obj.chunks():
            new_fo.write(chunk)
    return HttpResponse('--file upload success---')
