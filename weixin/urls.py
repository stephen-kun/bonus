from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^token', views.token, name='token'),
    url(r'^rcv_bonus',views.rcv_bonus, name='rcv_bonus'),
    url(r'^geted_bonus',views.geted_bonus, name='geted_bonus'),
    url(r'^asp_test',views.asp_test, name='asp_test'),
]
