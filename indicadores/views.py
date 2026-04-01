from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import OperacionMensualForm, ContractualMensualForm
from .models import OperacionMensual, ContractualMensual
from segmentacion.models import Cliente, Pais


@login_required(login_url='login')
def cargar_operacion(request, id_cliente, id_pais):
    # Obtenemos los objetos para validar que existen y para usarlos en el template
    cliente_obj = get_object_or_404(Cliente, pk=id_cliente)
    pais_obj = get_object_or_404(Pais, pk=id_pais)

    if request.method == 'POST':
        form = OperacionMensualForm(request.POST, user=request.user)
        if form.is_valid():
            operacion = form.save(commit=False)
            
            # Asignamos los objetos de FK que ya validamos arriba
            operacion.id_cliente = cliente_obj
            operacion.id_pais = pais_obj
            
            # Datos adicionales
            operacion.fecha_periodo = form.cleaned_data['fecha_periodo']
            operacion.creado_por = request.user 
            
            operacion.save()
            
            # Mensaje de éxito para el Toast
            messages.success(request, f"Operación de {cliente_obj.nombre_cliente} ({pais_obj.nombre_pais}) cargada con éxito.")
            return redirect('home')
        else:
            # Si el formulario falla (ej: combinación duplicada en clean), mandamos el error al Toast
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        # Iniciamos el formulario vacío
        form = OperacionMensualForm(user=request.user)
    
    return render(request, 'indicadores/form_operacion.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj
    })

@login_required(login_url='login')
def cargar_contractual(request, id_cliente, id_pais):
    # Validamos existencia de cliente y país
    cliente_obj = get_object_or_404(Cliente, pk=id_cliente)
    pais_obj = get_object_or_404(Pais, pk=id_pais)

    if request.method == 'POST':
        form = ContractualMensualForm(request.POST)
        if form.is_valid():
            contractual = form.save(commit=False)
            
            # Asignación de llaves foráneas y auditoría
            contractual.id_cliente = cliente_obj
            contractual.id_pais = pais_obj
            contractual.fecha_periodo = form.cleaned_data['fecha_periodo']
            contractual.creado_por = request.user 
            contractual.fecha_contrato_modificacion = timezone.now().date()
            
            contractual.save()
            
            messages.success(request, f"Metas contractuales de {cliente_obj.nombre_cliente} ({pais_obj.nombre_pais}) guardadas.")
            return redirect('home')
        else:

            for field, errors in form.errors.items():
                            for error in errors:
                                # Esto hace que el error aparezca en la esquina
                                messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        # Pre-rellenamos los IDs para que el formulario sea válido al enviarse
        form = ContractualMensualForm(initial={'id_cliente': cliente_obj, 'id_pais': pais_obj})
    
    return render(request, 'indicadores/form_contractual.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj
    })

# Una vista auxiliar para manejar la redirección del acordeón
@login_required
def redireccionar_carga(request, tipo):
    if request.method == 'POST':
        combo = request.POST.get('asignacion_id') # Viene como "1-10"
        pais_id, cliente_id = combo.split('-')
        
        if tipo == 'operacion':
            return redirect('cargar_operacion', id_cliente=cliente_id, id_pais=pais_id)
        elif tipo == 'contractual':
            return redirect('cargar_contractual', id_cliente=cliente_id, id_pais=pais_id)
        else:
            # Aquí redirigirías a cargar_contractual cuando la tengamos
            return redirect('home')
    return redirect('home')


#EDICION DE FORMULARIOS

@login_required(login_url='login')
def editar_operacion(request, pk):
    operacion = get_object_or_404(OperacionMensual, pk=pk)

    if request.method == 'POST':
        form = OperacionMensualForm(request.POST, instance=operacion, user=request.user)
        if form.is_valid():
            edit_obj = form.save(commit=False)
            edit_obj.modificado_por = request.user
            edit_obj.save()
            
            messages.success(request, f"Cambios en {operacion.id_cliente.nombre_cliente} guardados correctamente.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request,f"Error en {field}:{error}")
    else:
        form = OperacionMensualForm(instance=operacion, user=request.user)

    return render(request, 'indicadores/form_operacion.html', {
        'form': form,
        'operacion': operacion,
        'es_edicion': True,
        'cliente':operacion.id_cliente,
        'pais':operacion.id_pais,

    })

@login_required(login_url='login')
def lista_operaciones(request):
    if request.user.es_administrador_global:
        queryset=OperacionMensual.objects.all()
    else:
        queryset=OperacionMensual.objects.filter(creado_por=request.user)

    operaciones = queryset.select_related(
        'id_cliente',
        'id_pais',
        'creado_por',
        'modificado_por'
    ).order_by('-fecha_periodo','-fecha_creacion')
    return render(request,'indicadores/lista_operaciones.html',{
        'operaciones':operaciones
    })


# indicadores/views.py

@login_required(login_url='login')
def editar_contractual(request, pk):
    contractual = get_object_or_404(ContractualMensual, pk=pk)
    if request.method == 'POST':
        form = ContractualMensualForm(request.POST, instance=contractual, user=request.user)
        if form.is_valid():
            edit_obj = form.save(commit=False)
            edit_obj.modificado_por = request.user
            edit_obj.save()
            
            messages.success(request, f"Metas de {contractual.id_cliente.nombre_cliente} actualizadas correctamente.")
            return redirect('home') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {form.fields[field].label}: {error}")
    else:
        form = ContractualMensualForm(instance=contractual, user=request.user)
    return render(request, 'indicadores/form_contractual.html', {
        'form': form,
        'contractual': contractual,
        'es_edicion': True,
        'cliente': contractual.id_cliente,
        'pais': contractual.id_pais,
    })

@login_required(login_url='login')
def lista_contractual(request):
    if request.user.es_administrador_global:
        queryset = ContractualMensual.objects.all()
    else:
        queryset = ContractualMensual.objects.filter(creado_por=request.user)

    contractuales = queryset.select_related(
        'id_cliente', 
        'id_pais', 
        'creado_por', 
        'modificado_por'
    ).order_by('-fecha_periodo', '-fecha_creacion')

    return render(request, 'indicadores/lista_contractual.html', {
        'contractuales': contractuales
    })