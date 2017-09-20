#!/usr/bin/python
#coding:utf-8
import json

import time

import datetime
from django.shortcuts import redirect, render_to_response,render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from users.permission import PermissionVerify
from zhishutang.common.CommonPaginator import SelfPaginator


from users.models import User,PermissionList,RoleList


@login_required
@PermissionVerify()
def index(request):
    return render_to_response('main/index.html',locals(),RequestContext(request))

@login_required
@PermissionVerify()
def html(request):
    return render_to_response('main/no.html',locals(),RequestContext(request))

@login_required
def Home(request):
    iUser = User.objects.get(username=request.user)
    return render_to_response('main/home.html',locals(),RequestContext(request))



