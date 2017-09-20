# __*__ coding: utf-8 __*__

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from zhishutang.common.CommonPaginator import SelfPaginator

from users.forms import PermissionListForm
from users.models import User,RoleList,PermissionList


def PermissionVerify():
    '''权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    '''
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iUser = User.objects.get(username=request.user)

            if not iUser.is_superuser: #判断用户如果是超级管理员则具有所有权限
                if not iUser.role: #如果用户无角色，直接返回无权限
                    return HttpResponseRedirect(reverse('permissiondenyurl'))

                role_permission = RoleList.objects.get(name=iUser.role)
                role_permission_list = role_permission.permission.all()

                matchUrl = []
                for x in role_permission_list:
                    if request.path == x.url or request.path.rstrip('/') == x.url: #精确匹配，判断request.path是否与permission表中的某一条相符
                        matchUrl.append(x.url)
                    elif request.path.startswith(x.url): #判断request.path是否以permission表中的某一条url开头
                        matchUrl.append(x.url)
                    else:
                        pass

                if len(matchUrl) == 0:
                    return HttpResponseRedirect(reverse('permissiondenyurl'))
            else:
                pass

            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator

