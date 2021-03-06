from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import hashlib
from .models import User
# Create your views here.
def reg_view(request):
    # 注册
    if request.method == 'GET':
        return render(request,'user/register.html')

    elif request.method == 'POST':
        # 处理提交数据
        username = request.POST.get('username')
        if not username:
            username_error = 'please give me username'
            return render(request,'user/register.html',locals())

        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if not password_1 or not password_2:
            password_1_error = 'please give me password!'
            return render(request,'user/register.html',locals())

        if password_1 != password_2:
            password_2_error = 'The password not same !!'
            return render(request,'user/register.html',locals())

        # hash密码版本
        # 1. 先生成hash算法对象
        # m = hashlib.md5()
        # 2. 将明文update到对象中  注意:py3 要求输入明文为字节串[b串]
        # m.update(password_1.encode())
        # 3. 调用对象的 hexdigest[16进制]或digest[2进制];通常用16进制
        # password_m = m.hexdigest()
        # print(password_m)

        # 查询用户是否存在
        try:
            old_user = User.objects.get(username = username)
            # 当前用户名已被注册
            username_error = 'The username is existed !'
            return render(request,'user/register.html',locals())
        except Exception as e:
            # 没有查到的情况下 报错 证明当前用户名为可用状态
            print('---%s get error is %s'%(username,e))
            try:
                user = User.objects.create(username = username,
                                           password = password_1)
                html  = '''
                        注册成功 点击<a href="/note/index">进入首页
                '''
                # 存 session
                request.session['username'] = username

                return HttpResponse(html)
            except Exception as e:
                print(e)
                username_error = 'The name is existed !!!'
                return render(request,'user/register.html',locals())

def login_view(request):
    if request.method == 'GET':
        # 拿页面
        # 1 先检查session
        if 'username' in request.session:
            return HttpResponseRedirect('/note/index')
        # 2 检查cookie
        if 'username' in request.COOKIES:
           # 赋值回 session
            request.session['username'] = request.COOKIES['username']
            return HttpResponseRedirect('/note/index')
        return render(request,'user/login.html')
    elif request.method == 'POST':
        # 处理请求登录
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 密码 hash版
        # m = hashlib.md5
        # m.update(password.encode())
        # password_m = m.hexdigest()
        # user = User.objects.filter(username=username,password=password)

        user = User.objects.filter(username=username, password=password)

        if not user:
            # 用户名或密码错误
            error = '用户名或密码错误!'
            return render(request,'user/login.html',locals())
        # 由于使用了filter,返回值是个数组,并且用户名具备唯一索引,当前用户一定是该数组第一个元素
        user = user[0]
        # session and cookie 操作
        print(request.session)
        request.session['username'] = username
        print(request.session['username'])

        resp = HttpResponseRedirect('/note/index')

        if 'isSaved' in request.POST.keys():
            # 证明用户选择保持长期登录状态[7天]
            resp.set_cookie('username', username, 60 * 60 * 24 * 7)
        return resp

def logout_view(request):
    # 登出/注销
    # 删除session
    if 'username' in request.session:
        del request.session['username']
    resp = HttpResponseRedirect('/note/index')

    # 删除cookie
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    return resp

def user_test(request):

    return HttpResponse('Hi,Welcome to here ~')


