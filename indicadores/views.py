from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OperacionMensualForm

@login_required(login_url='login')
def cargar_operacion(request):
    if request.method == 'POST':
        form = OperacionMensualForm(request.POST, user=request.user)
        if form.is_valid():
            operacion = form.save(commit=False)
            
            # Asignamos la fecha que construimos en el método 'clean' del formulario
            operacion.fecha_periodo = form.cleaned_data['fecha_periodo']
            
            # Asignación automática de auditoría
            operacion.creado_por = request.user 
            
            operacion.save()
            return redirect('home')
    else:
        form = OperacionMensualForm(user=request.user)
    
    return render(request, 'indicadores/form_operacion.html', {'form': form})