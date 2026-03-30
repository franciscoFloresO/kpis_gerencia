from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UsuarioClientePais, UsuarioApp
from .decorators import admin_required
from .forms import UsuarioAppForm



#AUTENTICACION
def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)

        if user is not None:
            if user.estado_activo:
                login(request, user)
                return redirect('selector_contexto')
            else:
                messages.error(request, "Esta cuenta está desactivada.")
        else:
            messages.error(request, "Credenciales incorrectas o cuenta inactiva.")
    
    return render(request, 'segmentacion/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#USUARIOS

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioAppForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    else:
        form = UsuarioAppForm()

    return render(request,'segmentacion/crear_usuario.html',{'form':form})

def lista_usuarios(request):
    usuarios = UsuarioApp.objects.all()
    return render(request, 'segmentacion/lista_usuarios.html', {'usuarios':usuarios})

def editar_usuario(request, id_usuario):
    usuario = UsuarioApp.objects.get(id_usuario=id_usuario)

    if request.method == 'POST':
        form = UsuarioAppForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
        
    else:
        form = UsuarioAppForm(instance=usuario)

    return render(request, 'segmentacion/crear_usuario.html',{
        'form':form,
        'editando':True
    })



#EXTRAS

@login_required(login_url='login')
def home(request):
    # Esta vista ahora solo sirve para mostrar las dos opciones de carga
    return render(request, 'segmentacion/home.html')

@login_required(login_url='login')
def selector_contexto(request):
    usuario = request.user
    
    if usuario.es_administrador_global:
        # El admin ve todas las asignaciones existentes
        asignaciones = UsuarioClientePais.objects.all()
    else:
        # Usuario normal ve solo lo suyo
        asignaciones = UsuarioClientePais.objects.filter(usuario=usuario, estado_activo=True)

    return render(request, 'segmentacion/selector.html', {'asignaciones': asignaciones})

