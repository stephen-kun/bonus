from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from weixin.models import Consumer

User = get_user_model()


class AuthBackend(object):
    def authenticate(self, open_id=None):
        if not open_id:
            return None
        else:
            try:
                consumer = Consumer.objects.get(open_id=open_id)
                user = User.objects.get(id=consumer.user.id)
                return user
            except Exception as ex:
                return None

    def get_user(self, id):
        if not id:
            return None
        try:
            user = User.objects.get(id=id)
            return user
        except Exception as ex:
            return None
