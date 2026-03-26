from django.shortcuts import render
from .models import Pais, Cliente

def lista_paises(request):
    # Obtenemos todos los países de la base de datos
    paises = Pais.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'catalogo/lista.html', {
        'paises': paises,
        'clientes':clientes})