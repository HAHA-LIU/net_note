from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from note.models import Note
from user.models import User
from . import models


def note_index(request):
    if request.method == 'GET':
        return render(request,'note/index.html',locals())

def list_view(request):
    if request.method == 'GET':
        user = request.session['username']
        user = models.User.objects.get(username=user)
        all_note = models.Note.objects.filter(user=user)
        return render(request,'note/list_note.html',locals())

def check_logging(fn):
    def wrap(request,*args,**kwargs):
        #检查用户是否登录
            # 1 先检查session
        if 'username' not in request.session:
            if 'username' not in request.COOKIES:
                return HttpResponseRedirect('/user/login')
            else:
                # 赋值回 session
                request.session['username'] = request.COOKIES['username']
        return fn(request,*args,**kwargs)
    return wrap

@check_logging
def add_view(request):
    if request.method == 'GET':
        return render(request,'note/add_note.html')
    elif request.method == 'POST':
        # 处理提交数据
        title = request.POST.get('title')
        content =  request.POST.get('content')
        # 存数据
        username = request.session.get('username')
        user = User.objects.get(username = username)
        note = Note(user=user)
        note.title = title
        note.content = content
        note.save()
        return HttpResponseRedirect('/note/')

@check_logging
def mod_view(request,id):
    user = request.session['username']
    user = User.objects.get(username=user)
    note = models.Note.objects.get(user=user, id=id)
    if request.method == 'GET':
        return render(request,'note/mod_note.html',locals())
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        note.title = title
        note.content = content
        note.save()
        return HttpResponseRedirect('/note')

@check_logging
def con_view(request,id):
    user = request.session['username']
    user = User.objects.get(username=user)
    note = models.Note.objects.get(user=user, id=id)
    if request.method == 'GET':
        return render(request, 'note/content_note.html', locals())

@check_logging
def del_view(request,id):
    user_name = request.session['username']
    print(user_name)
    user = User.objects.get(username=user_name)
    note = models.Note.objects.get(user=user,id=int(id))
    note.delete()
    return HttpResponseRedirect('/note')

@check_logging
def page_test(request):
    # 测试分页功能
    notes = Note.objects.all()
    paginator = Paginator(notes,2)
    current_p = request.GET.get('page', 1)

    page = paginator.page(int(current_p))
    return render(request,'note/page_test.html',locals())

