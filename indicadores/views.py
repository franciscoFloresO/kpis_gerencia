from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OperacionMensualForm, ContractualMensualForm
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
            
            contractual.save()
            
            messages.success(request, f"Metas contractuales de {cliente_obj.nombre_cliente} ({pais_obj.nombre_pais}) guardadas.")
            return redirect('home')
        else:
            # Enviamos errores al Toast de la esquina
            for error in form.non_field_errors():
                messages.error(request, error)
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