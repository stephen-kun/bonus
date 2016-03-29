from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^token', views.token, name='token'),
    url(r'^get_bonus',views.get_bonus, name='get_bonus'),
]
