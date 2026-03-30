# segmentacion/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import UsuarioApp

class UsuarioAppBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UsuarioApp.objects.get(usuario_login=username)
            
            if check_password(password, user.password) and user.estado_activo:
                return user
        except UsuarioApp.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UsuarioApp.objects.get(pk=user_id)
        except UsuarioApp.DoesNotExist:
            return None