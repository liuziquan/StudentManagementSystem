from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^audit_log/$', views.audit_log, name='audit_log'),
]