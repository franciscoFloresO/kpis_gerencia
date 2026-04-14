from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import OperacionMensualForm, ContractualMensualForm, OperacionMensualFSForm, ContractualMensualFSForm, MultaForm
from .models import OperacionMensual, ContractualMensual, OperacionMensualFS, ContractualMensualFS, Multa
from segmentacion.models import Cliente, Pais, UsuarioClientePais


@login_required(login_url='login')
def cargar_operacion(request, id_cliente, id_pais):
    cliente_obj = get_object_or_404(Cliente, pk=id_cliente)
    pais_obj = get_object_or_404(Pais, pk=id_pais)

    if request.method == 'POST':
        form = OperacionMensualForm(request.POST, user=request.user)
        if form.is_valid():
            operacion = form.save(commit=False)
            operacion.id_cliente = cliente_obj
            operacion.id_pais = pais_obj
            operacion.codigo_moneda = 'USD'
            operacion.fecha_periodo = form.cleaned_data['fecha_periodo']
            operacion.creado_por = request.user 
            
            operacion.save()
            
            messages.success(request, f"Operación de {cliente_obj.nombre_cliente} ({pais_obj.nombre_pais}) cargada con éxito.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        label = form.fields[field].label if field in form.fields else field
                        messages.error(request, f"Error en {label}: {error}")
    else:
        form = OperacionMensualForm(user=request.user, initial={
            'id_cliente': cliente_obj,
            'id_pais': pais_obj,
            'codigo_moneda':'USD'
        })
    
    return render(request, 'indicadores/form_operacion.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj
    })


@login_required(login_url='login')
def cargar_operacion_fs(request, id_cliente, id_pais):
    cliente_obj = get_object_or_404(Cliente, pk=id_cliente)
    pais_obj = get_object_or_404(Pais, pk=id_pais)

    if request.method == 'POST':
        # Se pasa user=request.user para mantener la firma del Form homologado
        form = OperacionMensualFSForm(request.POST, user=request.user)
        if form.is_valid():
            operacion = form.save(commit=False)
            
            # Homologación de nombres de campos según el modelo nuevo
            operacion.id_cliente = cliente_obj
            operacion.id_pais = pais_obj
            operacion.codigo_moneda = 'USD'
            operacion.fecha_periodo = form.cleaned_data['fecha_periodo']
            operacion.creado_por = request.user 
            
            operacion.save()
            
            messages.success(request, f"Operación Field Services de {cliente_obj.nombre_cliente} ({pais_obj.nombre_pais}) cargada con éxito.")
            return redirect('home')
        else:
            # Se replica exactamente el control de errores de la vista original
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        label = form.fields[field].label if field in form.fields else field
                        messages.error(request, f"Error en {label}: {error}")
    else:
        # Se replican los valores iniciales y el paso del usuario
        form = OperacionMensualFSForm(user=request.user, initial={
            'id_cliente': cliente_obj,
            'id_pais': pais_obj,
            'codigo_moneda': 'USD'
        })
    
    return render(request, 'indicadores/form_operacion_fs.html', {
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

@login_required(login_url='login')
def cargar_contractual_fs(request, id_cliente, id_pais):
    # Validamos existencia de cliente y país
    cliente_obj = get_object_or_404(Cliente, pk=id_cliente)
    pais_obj = get_object_or_404(Pais, pk=id_pais)

    if request.method == 'POST':
        # Se agrega user=request.user para que coincida con el constructor del Form homologado
        form = ContractualMensualFSForm(request.POST, user=request.user)
        if form.is_valid():
            contractual = form.save(commit=False)
            
            # Asignación de llaves foráneas y auditoría (nombres homologados)
            contractual.id_cliente = cliente_obj
            contractual.id_pais = pais_obj
            contractual.fecha_periodo = form.cleaned_data['fecha_periodo']
            contractual.creado_por = request.user 
            contractual.fecha_contrato_modificacion = timezone.now().date()
            
            contractual.save()
            
            messages.success(request, f"Metas contractuales FS de {cliente_obj.nombre_cliente} ({pais_obj.nombre_pais}) guardadas.")
            return redirect('home')
        else:
            # Réplica exacta del manejo de errores de la vista original
            for field, errors in form.errors.items():
                for error in errors:
                    label = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"{label}: {error}")
    else:
        # Pre-rellenamos los IDs y pasamos el usuario para inicializar el formulario
        form = ContractualMensualFSForm(user=request.user, initial={
            'id_cliente': cliente_obj, 
            'id_pais': pais_obj
        })
    
    return render(request, 'indicadores/form_contractual_fs.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj,
        'es_edicion': False  # Ayuda al template a distinguir entre carga y edición
    })




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
def editar_operacion_fs(request, pk):
    operacion = get_object_or_404(OperacionMensualFS, pk=pk)
    cliente_obj = operacion.id_cliente
    pais_obj = operacion.id_pais

    if request.method == 'POST':
        form = OperacionMensualFSForm(request.POST, instance=operacion, user=request.user)
        if form.is_valid():
            op_editada = form.save(commit=False)
            op_editada.modificado_por = request.user
            op_editada.save()
            messages.success(request, "Registro de operación FS actualizado correctamente.")
            return redirect('lista_operaciones_fs')
    else:
        form = OperacionMensualFSForm(instance=operacion, user=request.user)

    return render(request, 'indicadores/form_operacion_fs.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj,
        'es_edicion': True,
        'operacion': operacion
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

@login_required(login_url='login')
def lista_operaciones_fs(request):
    if request.user.es_administrador_global:
        queryset = OperacionMensualFS.objects.all()
    else:
        queryset = OperacionMensualFS.objects.filter(creado_por=request.user)

    operaciones_fs = queryset.select_related(
        'id_cliente',
        'id_pais',
        'creado_por',
        'modificado_por'
    ).order_by('-fecha_periodo', '-fecha_creacion')

    return render(request, 'indicadores/lista_operaciones_fs.html', {
        'operaciones_fs': operaciones_fs
    })


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
def editar_contractual_fs(request, pk):
    contractual = get_object_or_404(ContractualMensualFS, pk=pk)
    cliente_obj = contractual.id_cliente
    pais_obj = contractual.id_pais

    if request.method == 'POST':
        form = ContractualMensualFSForm(request.POST, instance=contractual, user=request.user)
        if form.is_valid():
            con_editado = form.save(commit=False)
            con_editado.modificado_por = request.user
            con_editado.fecha_contrato_modificacion = timezone.now().date()
            con_editado.save()
            messages.success(request, "Metas contractuales FS actualizadas.")
            return redirect('lista_contractual_fs')
    else:
        form = ContractualMensualFSForm(instance=contractual, user=request.user)

    return render(request, 'indicadores/form_contractual_fs.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj,
        'es_edicion': True
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

@login_required(login_url='login')
def lista_contractual_fs(request):
    if request.user.es_administrador_global:
        queryset = ContractualMensualFS.objects.all()
    else:
        queryset = ContractualMensualFS.objects.filter(creado_por=request.user)
    contractuales_fs = queryset.select_related(
        'id_cliente', 
        'id_pais', 
        'creado_por', 
        'modificado_por'
    ).order_by('-fecha_periodo', '-fecha_creacion')

    return render(request, 'indicadores/lista_contractual_fs.html', {
        'contractuales_fs': contractuales_fs
    })


# Una vista auxiliar para manejar la redirección del acordeón
@login_required
def redireccionar_carga(request, tipo):
    if request.method == 'POST':
        combo = request.POST.get('asignacion_id')
        tipo_servicio = request.POST.get('tipo_servicio') # Captura SD o FS
        
        if not combo:
            return redirect('home')
            
        pais_id, cliente_id = combo.split('-')
        
        if tipo == 'operacion':
            # Decide entre la vista clásica (SD) o la nueva (FS)
            nombre_url = 'cargar_operacion_fs' if tipo_servicio == 'FS' else 'cargar_operacion'
            return redirect(nombre_url, id_cliente=cliente_id, id_pais=pais_id)
            
        elif tipo == 'contractual':
            # Decide entre la vista clásica (SD) o la nueva (FS)
            nombre_url = 'cargar_contractual_fs' if tipo_servicio == 'FS' else 'cargar_contractual'
            return redirect(nombre_url, id_cliente=cliente_id, id_pais=pais_id)
        
        elif tipo == 'multa':
            # Para multas usamos una vista única, ya que el servicio se elige dentro del form
            return redirect('cargar_multa', id_cliente=cliente_id, id_pais=pais_id)
        
            
    return redirect('home')



@login_required(login_url='login')
def cargar_multa(request, id_cliente, id_pais):
    # Validamos existencia de cliente y país
    cliente_obj = get_object_or_404(Cliente, pk=id_cliente)
    pais_obj = get_object_or_404(Pais, pk=id_pais)

    if request.method == 'POST':
        form = MultaForm(request.POST)
        if form.is_valid():
            multa = form.save(commit=False)
            
            multa.id_cliente = cliente_obj
            multa.id_pais = pais_obj
            multa.fecha_periodo = form.cleaned_data['fecha_periodo']
            
            multa.creado_por = request.user 
            
            multa.save()
            
            messages.success(request, f"Multa para {cliente_obj.nombre_cliente} registrada con éxito.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    label = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"Error en {label}: {error}")
    else:
        form = MultaForm(initial={
            'id_cliente': cliente_obj, 
            'id_pais': pais_obj
        })
    
    return render(request, 'indicadores/form_multa.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj,
        'es_edicion': False
    })

@login_required(login_url='login')
def gestion_multas(request):
    if request.user.es_administrador_global:
        asignaciones = UsuarioClientePais.objects.filter(estado_activo=True).select_related('cliente', 'pais')
    else:
        asignaciones = UsuarioClientePais.objects.filter(
            usuario=request.user, 
            estado_activo=True
        ).select_related('cliente', 'pais')
    
    if request.user.es_administrador_global:
        multas = Multa.objects.all()
    else:
        multas = Multa.objects.filter(creado_por=request.user)
        
    multas = multas.select_related('id_cliente', 'id_pais', 'creado_por').order_by('-fecha_periodo')

    return render(request, 'indicadores/gestion_multas.html', {
        'asignaciones': asignaciones,
        'multas': multas
    })

@login_required(login_url='login')
def editar_multa(request, pk):
    # Recuperamos la multa o lanzamos 404
    multa = get_object_or_404(Multa, pk=pk)
    cliente_obj = multa.id_cliente
    pais_obj = multa.id_pais

    if request.method == 'POST':
        # Pasamos la instancia al formulario
        form = MultaForm(request.POST, instance=multa)
        if form.is_valid():
            multa_editada = form.save(commit=False)
            
            # Si agregaste campos de auditoría al modelo:
            # multa_editada.modificado_por = request.user
            
            multa_editada.save()
            
            messages.success(request, f"Registro de multa actualizado correctamente.")
            return redirect('gestion_multas')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    label = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"Error en {label}: {error}")
    else:
        # Al ser GET, el __init__ del formulario cargará mes y año desde fecha_periodo
        form = MultaForm(instance=multa)

    return render(request, 'indicadores/form_multa.html', {
        'form': form,
        'cliente': cliente_obj,
        'pais': pais_obj,
        'es_edicion': True,
        'multa': multa
    })