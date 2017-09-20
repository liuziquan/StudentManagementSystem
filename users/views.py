#!/usr/bin/python
#coding:utf-8

from django.shortcuts import redirect, render_to_response,render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse

from zhishutang.common.CommonPaginator import SelfPaginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

from users.permission import PermissionVerify

from django.contrib import auth
from django.contrib.auth import get_user_model
from users.forms import LoginUserForm,ChangePasswordForm,AddUserForm,EditUserForm,PermissionListForm,RoleListForm
from users.models import User,PermissionList,RoleList
from auditlog.models import Message
from django.contrib.auth.hashers import make_password, check_password


def UserIP(request):
    ip = ''
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

@csrf_exempt
def LoginUser(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'GET' and request.GET.has_key('next'):
        next = request.GET['next']
    else:
        next = '/'

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            userid = User.objects.get(username=request.user)
            Message.objects.create(username=userid, type=u'用户登录', action=u'用户登录',
                                   action_ip=UserIP(request), content='%s 用户登录' % request.user)
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)

    kwvars = {
        'request':request,
        'form':form,
        'next':next,
    }

    return render_to_response('users/login.html',kwvars,RequestContext(request))

@csrf_exempt
def logout(request):
	auth.logout(request)
	return redirect("/users/login")

@csrf_exempt
def ChangePassword(request):
    if request.method=='POST':
        get_username = request.POST.get('username')
        get_mail = request.POST.get('mail')
        get_passwd = request.POST.get('password')
        get_setpassword = request.POST.get('setpassword')
        status = {}
        passwd = make_password(get_passwd, None, 'pbkdf2_sha256')
        User.objects.filter(username=get_username).update(password=passwd)

    return render(request, 'users/password.change.html')
    #return render_to_response('users/password.change.html',RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def ListUser(request):
    mList = get_user_model().objects.all()

    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('users/user.list.html',kwvars,RequestContext(request))

@csrf_exempt
def AddUser(request):

    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()

            return HttpResponseRedirect(reverse('listuserurl'))
    else:
        form = AddUserForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('users/register.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def EditUser(request,ID):
    user = get_user_model().objects.get(id = ID)
    print user

    if request.method=='POST':
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            userid = User.objects.get(username=request.user)
            username = User.objects.get(username=user)
            Message.objects.create(username=userid, type=u'信息修改', action=u'修改用户信息',
                                   action_ip=UserIP(request), content='修改%s用户信息' % username)
            return HttpResponseRedirect(reverse('listuserurl'))
    else:
        form = EditUserForm(instance=user
        )

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('users/user.edit.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def DeleteUser(request,ID):
    if ID == '1':
        return HttpResponse(u'超级管理员不允许删除!!!')
    else:
        get_user_model().objects.filter(id = ID).delete()

    return HttpResponseRedirect(reverse('listuserurl'))

@csrf_exempt
@login_required
def NoPermission(request):

    kwvars = {
        'request':request,
    }

    return render_to_response('users/permission.no.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def AddPermission(request):
    if request.method == "POST":
        form = PermissionListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listpermissionurl'))
    else:
        form = PermissionListForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('users/permission.add.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def ListPermission(request):
    mList = PermissionList.objects.all()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('users/permission.list.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def EditPermission(request,ID):
    iPermission = PermissionList.objects.get(id=ID)

    if request.method == "POST":
        form = PermissionListForm(request.POST,instance=iPermission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listpermissionurl'))
    else:
        form = PermissionListForm(instance=iPermission)

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('users/permission.edit.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def DeletePermission(request,ID):
    PermissionList.objects.filter(id = ID).delete()

    return HttpResponseRedirect(reverse('listpermissionurl'))

@csrf_exempt
@login_required
@PermissionVerify()
def AddRole(request):
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listroleurl'))
    else:
        form = RoleListForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('users/role.add.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def ListRole(request):
    mList = RoleList.objects.all()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('users/role.list.html',kwvars,RequestContext(request))

@csrf_exempt
@login_required
@PermissionVerify()
def EditRole(request,ID):
    iRole = RoleList.objects.get(id=ID)

    if request.method == "POST":
        form = RoleListForm(request.POST,instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listroleurl'))
    else:
        form = RoleListForm(instance=iRole)

    kwvars = {
        'ID':ID,
        'form':form,
        'request':request,
    }

    return render_to_response('users/role.edit.html',kwvars,RequestContext(request))

