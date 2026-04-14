from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import UsuarioClientePais, UsuarioApp
from .decorators import admin_required
from .forms import UsuarioAppForm, AsignacionForm



#AUTENTICACION
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)

        if user is not None:
            if user.estado_activo:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Esta cuenta está desactivada.")
        else:
            messages.error(request, "Credenciales incorrectas o cuenta inactiva.")
    
    return render(request, 'segmentacion/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#USUARIOS
@admin_required
@login_required
def crear_usuario(request):
    if request.method == 'POST':
        print(request.POST)
        form = UsuarioAppForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save() 
            messages.success(request, f"Usuario {nuevo_usuario.usuario_login} creado. Ahora asigna sus permisos.")
            return redirect('gestionar_asignaciones', id_usuario=nuevo_usuario.id_usuario)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    label = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"Error en {label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, f"Error: {error}")

    else:
        form = UsuarioAppForm()
    return render(request, 'segmentacion/crear_usuario.html', {'form': form})

@admin_required
@login_required
def lista_usuarios(request):
    usuarios = UsuarioApp.objects.all()
    return render(request, 'segmentacion/lista_usuarios.html', {'usuarios':usuarios})

@admin_required
@login_required
def editar_usuario(request, id_usuario):
    usuario_obj = get_object_or_404(UsuarioApp, pk=id_usuario)
    
    if request.method == 'POST':
        form = UsuarioAppForm(request.POST, instance=usuario_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario {usuario_obj.usuario_login} actualizado correctamente.")
            return redirect('lista_usuarios')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = UsuarioAppForm(instance=usuario_obj)

    return render(request, 'segmentacion/crear_usuario.html', {
        'form': form,
        'editando': True,
        'usuario_target': usuario_obj
    })

@login_required
@admin_required # Tu decorador de seguridad
def gestionar_asignaciones(request, id_usuario):
    usuario_obj = get_object_or_404(UsuarioApp, pk=id_usuario)
    asignaciones = UsuarioClientePais.objects.filter(usuario=usuario_obj).select_related('pais', 'cliente')

    if request.method == 'POST':
        form = AsignacionForm(request.POST, usuario=usuario_obj)
        if form.is_valid():
            nueva_asig = form.save(commit=False)
            nueva_asig.usuario = usuario_obj
            nueva_asig.estado_activo = True
            nueva_asig.save()
            
            # Mensaje de éxito para la esquina
            messages.success(request, f"Asignación de {nueva_asig.cliente} agregada correctamente.")
            return redirect('gestionar_asignaciones', id_usuario=id_usuario)
        else:
            # PUENTE DE ERRORES:
            # Enviamos los errores del formulario al sistema de mensajes
            for error in form.non_field_errors():
                messages.error(request, error)
            
            # Si quieres capturar errores de campos específicos (opcional)
            for field, field_errors in form.errors.items():
                if field != '__all__':
                    for error in field_errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = AsignacionForm(usuario=usuario_obj)

    return render(request, 'segmentacion/gestion_asignaciones.html', {
        'usuario_target': usuario_obj,
        'asignaciones': asignaciones,
        'form': form
    })
# Vista rápida para eliminar (desactivar) una asignación
@login_required
@admin_required
def eliminar_asignacion(request, id_asignacion):
    asig = get_object_or_404(UsuarioClientePais, pk=id_asignacion)
    id_user = asig.usuario.id_usuario
    messages.success(request, f"Asignación de {asig.cliente} eliminada correctamente.")
    asig.delete() # O podrías hacer asig.estado_activo = False si prefieres soft-delete
    return redirect('gestionar_asignaciones', id_usuario=id_user)


#EXTRAS

@login_required(login_url='login')
def home(request):
    asignaciones = UsuarioClientePais.objects.filter(usuario=request.user, estado_activo=True).select_related('pais','cliente')
    return render(request, 'segmentacion/home.html',{
        'asignaciones':asignaciones
    })

@login_required(login_url='login')
def selector_contexto(request):
    usuario = request.user
    
    if usuario.es_administrador_global:
        asignaciones = UsuarioClientePais.objects.all()
    else:
        asignaciones = UsuarioClientePais.objects.filter(usuario=usuario, estado_activo=True)

    return render(request, 'segmentacion/selector.html', {'asignaciones': asignaciones})

