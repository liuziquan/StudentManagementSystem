from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$',views.LoginUser, name = 'login'),
    url(r'^logout/$',views.logout, name = 'logout'),

    url(r'^register/$',views.AddUser, name = 'adduserurl'),
    url(r'^list/$',views.ListUser, name = 'listuserurl'),
    url(r'^delete/(?P<ID>\d+)/$', views.DeleteUser, name='deleteuserurl'),
    url(r'^edit/(?P<ID>\d+)/$', views.EditUser, name='edituserurl'),
    url(r'^changepasswd/$', views.ChangePassword, name='changepasswdurl'),

    url(r'^deny/$', views.NoPermission, name='permissiondenyurl'),
    
    url(r'^permission/add/$', views.AddPermission, name='addpermissionurl'),
    url(r'^permission/list/$', views.ListPermission, name='listpermissionurl'),
    url(r'^permission/edit/(?P<ID>\d+)/$', views.EditPermission, name='editpermissionurl'),
    url(r'^permission/delete/(?P<ID>\d+)/$', views.DeletePermission, name='deletepermissionurl'),

    url(r'^role/add/$', views.AddRole, name='addroleurl'),
    url(r'^role/list/$', views.ListRole, name='listroleurl'),
    url(r'^role/edit/(?P<ID>\d+)/$', views.EditRole, name='editroleurl'),
]