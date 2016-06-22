"""bonus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^test_wx/$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^test_wx/$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^test_wx/blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin

import category
import comment
import topic

urlpatterns = [
    url(r'^test_wx/admin/', admin.site.urls),
    url(r'^test_wx/weixin/', include('weixin.urls')),
    url(r'^test_wx/manager/', include('manager.urls')),

    url(r'^test_wx/$', "topic.views.index_active", name='index'),
    # url(r'^test_wx/home/',include('topic.urls')),
    url(r'^test_wx/category/', include("category.urls", namespace='category')),
    url(r'^test_wx/topic/', include("topic.urls", namespace='topic')),
    url(r'^test_wx/comment/', include("comment.urls", namespace='comment')),
    url(r'^test_wx/user/',include("user.urls",namespace='user')),
    url(r'^test_wx/wx/',include("wx.urls",namespace='wx')),
    url(r'^test_wx/qubaba/',include("qubaba.urls",namespace='qubaba')),

    url(r'^test_wx/media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
]
