# catalogo/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from segmentacion.models import UsuarioClientePais

#@login_required(login_url='login')
def lista_paises(request):
    usuario_actual = request.user 

    if usuario_actual.es_administrador_global:
        # El administrador ve TODOS los países directamente de la tabla Pais
        from catalogo.models import Pais
        paises_para_mostrar = Pais.objects.all()
        es_administrador_global = True
    else:
        # El usuario normal solo ve lo que tiene asignado
        paises_para_mostrar = UsuarioClientePais.objects.filter(
            usuario=usuario_actual, 
            estado_activo=True
        )
        es_administrador_global = False

    return render(request, 'catalogo/lista.html', {
        'lista': paises_para_mostrar,
        'es_admin': es_administrador_global
    })