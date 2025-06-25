# decorators.py
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def solo_trabajador(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'perfil') and request.user.perfil.tipo_usuario == 'trabajador':
            return view_func(request, *args, **kwargs)
        return redirect('menu')
    return wrapper
