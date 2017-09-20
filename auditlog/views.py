#!/usr/bin/python2.7
# __*__ coding: utf-8 __*__

from django.shortcuts import render

# Create your views here.

#import os, json, shutil, time, datetime, re, xlwt, StringIO

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from zhishutang import settings
from auditlog.models import Message
from users.models import User
from users.permission import PermissionVerify
from zhishutang.common.CommonPaginator import SelfPaginator


@csrf_exempt
@login_required
@PermissionVerify()
def audit_log(request):
    if request.is_ajax():
        action = request.get_full_path().split('&')[0].split('=')[1]
        if action == 'search':
            get_action_ip = request.GET.get('action_ip')
            get_username = request.GET.get('username')
            get_start_audit_time = request.GET.get('start_audit_time')
            get_end_audit_time = request.GET.get('end_audit_time')
            get_type = request.GET.get('type')
            status = {}
            if get_action_ip:
                status['action_ip'] = get_action_ip
            if get_username:
                userid = User.objects.get(username=get_username)
                status['username_id'] = userid
            if get_start_audit_time and get_end_audit_time:
                start_audit_time = get_start_audit_time
                end_audit_time = get_end_audit_time
                status['audit_time__range'] = (start_audit_time, end_audit_time)
            if get_type:
                status['type'] = get_type
            if len(status) == 0:
                logs = Message.objects.all().order_by('-id')
            else:
                logs = Message.objects.filter(**status)
            lst = SelfPaginator(request, logs, 20)
            kwvars = {
                'lPage': lst,
                'request': request,
            }
            return render_to_response('auditlog/audit_log_table.html', kwvars, RequestContext(request))
    else:
        logs = Message.objects.all().order_by('-id')
        lst = SelfPaginator(request, logs, 20)
        kwvars = {
            'lPage': lst,
            'request': request,
        }
        return render_to_response('auditlog/audit_log.html', kwvars, RequestContext(request))

    return render(request, 'auditlog/audit_log.html')