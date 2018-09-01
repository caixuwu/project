from django.shortcuts import render, redirect, HttpResponse
from dwebsocket import accept_websocket
# Create your views here.
from app01.models import *
import time, json, queue
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from threading import Thread,Lock


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_info_name = user_info.objects.all().values_list('username', 'password')
        if (username, password) in user_info_name:
            return HttpResponse('该用户已经存在！！！')
        else:
            user_info.objects.create_user(username=username, password=password)
            return redirect('/app01/login/')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['seinfo'] = '123456'
            request.session['username'] = username
            return redirect('/app01/charbox/')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def charbox(request):
    if request.session.get('seinfo') == '123456':
        My_friend = user_info.objects.all()
        My_group = group.objects.all()
        return render(request, 'charbox.html', locals())
    else:
        return render(request, 'login.html')


GLOBAL_MSG_QUEUES = {}
# lock = Lock()

@accept_websocket
def echo(request):
    if request.is_websocket():
        p2 = Thread(target=send_msg, args=(request,))
        p1 = Thread(target=get_new_msgs, args=(request,))
        p1.start()
        p2.start()
        p2.join()
        p1.join()
    else:
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'charbox.html')


def send_msg(request):
    for message in request.websocket:
        msg = message.decode('utf8')
        MSG = eval(msg)
        MSG['timestamp'] = time.time()
        if MSG['type'] == 'single':
            #如果是新用户就没有队列，所以要给个队列给新用户
            if not GLOBAL_MSG_QUEUES.get(int(MSG['to'])):
                GLOBAL_MSG_QUEUES[int(MSG['to'])] = queue.Queue()
            # with lock:
            GLOBAL_MSG_QUEUES[int(MSG['to'])].put(MSG)
        print(GLOBAL_MSG_QUEUES)
        # else:  # group
        #     # 找到这个组里的所有成员,把发给该组的消息发给所有成员
        #     group_obj = group.objects.get(id=int(msg_data['to']))
        #     for member in group_obj.members.select_related():
        #         if not GLOBAL_MSG_QUEUES.get(member.id):
        #             GLOBAL_MSG_QUEUES[member.id] = queue.Queue()
        #         if member.id != request.user.userprofile.id:
        #             GLOBAL_MSG_QUEUES[member.id].put(msg_data)


def get_new_msgs(request):
    print(456)
    # 先判断自己有没有queue,如果是新用户第一次登录就是没有queue
    if request.user.id not in GLOBAL_MSG_QUEUES:
        GLOBAL_MSG_QUEUES[request.user.id] = queue.Queue()  # 创建一个queue
    q_obj = GLOBAL_MSG_QUEUES[request.user.id]
    while True:
        msg_list = []
        msg_count = GLOBAL_MSG_QUEUES[request.user.id].qsize()  # 获取queue的大小
        time.sleep(0.1)
        if msg_count > 0:
            for msg in range(msg_count):
                msg_list.append(q_obj.get())  # q_obj.get()不需要指定参数,会找最旧的那一条
            print("new msgs:", msg_list)
            request.websocket.send(str(msg_list).encode('utf8'))

#
