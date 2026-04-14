from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def _wrapped_view(request, *args, ** kwargs):
        if request.user.is_authenticated and request.user.es_administrador_global:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view