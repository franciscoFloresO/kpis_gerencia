# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('paises/', views.lista_paises, name='lista_paises'),
]