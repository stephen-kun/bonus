"""bonus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin

import category
import comment
import topic

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^weixin/', include('weixin.urls')),
    url(r'^manager/', include('manager.urls')),

    url(r'^$', "topic.views.index_active", name='index'),
    # url(r'^home/',include('topic.urls')),
    url(r'^category/', include("category.urls", namespace='category')),
    url(r'^topic/', include("topic.urls", namespace='topic')),
    url(r'^comment/', include("comment.urls", namespace='comment')),
    url(r'^user/',include("user.urls",namespace='user')),
    url(r'^wx/',include("wx.urls",namespace='wx')),
    url(r'^qubaba/',include("qubaba.urls",namespace='qubaba')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
]
