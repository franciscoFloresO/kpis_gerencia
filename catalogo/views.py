# catalogo/views.py
from django.contrib.auth.decorators import login_required
from segmentacion.models import UsuarioClientePais
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ClienteForm, PaisForm
from .models import Cliente, Pais
from .decorators import admin_required

@admin_required
@login_required
def lista_clientes(request):
    if not request.user.es_administrador_global:
        return redirect('home')
    
    # Obtenemos todos los clientes del catálogo
    clientes = Cliente.objects.all().order_by('nombre_cliente')
    
    return render(request, 'catalogo/lista_cliente.html', {
        'clientes': clientes
    })

@admin_required
@login_required
def crear_cliente(request):
    # Verificamos que sea administrador (usando el campo de tu UsuarioApp)
    if not request.user.es_administrador_global:
        messages.error(request, "No tiene permisos para realizar esta acción.")
        return redirect('home')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado exitosamente en el sistema.")
            return redirect('lista_clientes') 
    else:
        form = ClienteForm()

    return render(request, 'catalogo/form_cliente.html', {'form': form})

@admin_required
@login_required
def editar_cliente(request, pk):
    if not request.user.es_administrador_global:
        return redirect('home')

    cliente_obj = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cliente '{cliente_obj.nombre_cliente}' actualizado correctamente.")
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente_obj)

    return render(request, 'catalogo/form_cliente.html', {
        'form': form,
        'cliente': cliente_obj,
        'es_edicion': True # Para cambiar el título en el HTML
    })

@admin_required
@login_required
def lista_paises(request):
    if not request.user.es_administrador_global:
        return redirect('home')
    paises = Pais.objects.all().order_by('nombre_pais')
    return render(request, 'catalogo/lista_paises.html', {'paises': paises})

@admin_required
@login_required
def crear_pais(request):
    if not request.user.es_administrador_global:
        return redirect('home')
    if request.method == 'POST':
        form = PaisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "País creado exitosamente.")
            return redirect('lista_paises')
    else:
        form = PaisForm()
    return render(request, 'catalogo/form_pais.html', {'form': form, 'es_edicion': False})

@admin_required
@login_required
def editar_pais(request, pk):
    if not request.user.es_administrador_global:
        return redirect('home')
    pais_obj = get_object_or_404(Pais, pk=pk)
    if request.method == 'POST':
        form = PaisForm(request.POST, instance=pais_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"País '{pais_obj.nombre_pais}' actualizado.")
            return redirect('lista_paises')
    else:
        form = PaisForm(instance=pais_obj)
    return render(request, 'catalogo/form_pais.html', {'form': form, 'pais': pais_obj, 'es_edicion': True})