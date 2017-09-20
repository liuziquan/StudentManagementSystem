#!/usr/bin/python2.7
# __*__ coding: utf-8 __*__


from __future__ import unicode_literals

from django.db import models

# Create your models here.

import datetime
from django.db import models
from users.models import User


class Message(models.Model):

    audit_time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    type = models.CharField(max_length=10, verbose_name=u'类型')
    action = models.CharField(max_length=50, verbose_name=u'动作')
    action_ip = models.CharField(max_length=15, verbose_name=u'执行IP')
    content = models.CharField(max_length=50, verbose_name=u'内容')
    username = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = u'日志信息管理'