from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^token', views.token, name='token'),
    url(r'^rcv_bonus',views.rcv_bonus, name='rcv_bonus'),
    url(r'^view_geted_bonus',views.view_geted_bonus, name='view_geted_bonus'),
    url(r'^snd_bonus',views.snd_bonus, name='snd_bonus'),
    url(r'^redirect_bonus_snd',views.redirect_bonus_snd, name='redirect_bonus_snd'),
    url(r'^view_rcv_bonus',views.view_rcv_bonus, name='view_rcv_bonus'),
    url(r'^view_redirect_bonus_rcv',views.view_redirect_bonus_rcv, name='view_redirect_bonus_rcv'),
    url(r'^view_action_get_bonus',views.view_action_get_bonus, name='view_action_get_bonus'),
]
