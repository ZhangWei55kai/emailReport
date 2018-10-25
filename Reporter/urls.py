"""Reporter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from imgReport import views
from django.views.static import serve
import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index),
    url(r'^getPro/(?P<proId>\d+)',views.getProjectVer),
    url(r'^isSonVerOrParVer/(?P<proId>\d+)/(?P<Vname>.*)',views.isSonVerOrParVer),
    url(r'^getAllBug/(?P<verId>\d+)',views.getAllBug),
    url(r'^getChildVerBug/',views.getChildVerBug),
    url(r'^sendEmail/',views.sendEmailByContext),
    url(r'^getEmailInfo/',views.getEmailInfo),
    url(r'^saveEmailText/',views.saveEmail),
    url(r'userLogin/',views.userLogin.as_view()),
    url(r'getLoginPage/',views.getLoginPage.as_view()),
    url(r'getRegisterPage/',views.getRegisterPage.as_view()),
    url(r'getIndexPage/',views.getIndexPage.as_view()),
    url(r'logout/',views.Logout.as_view()),
    url(r'getUserPage/',views.getPermissionPage.as_view()),
    url(r'getUserinfo/',views.getUserinfo),
    url(r'createPer/',views.createPermission.as_view()),
    url(r'getPer',views.getPermisionList),
    url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
]
