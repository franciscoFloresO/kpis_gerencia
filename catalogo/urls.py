# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('paises/', views.lista_paises, name='lista_paises'),
    path('paises/nuevo/', views.crear_pais, name='crear_pais'),
    path('paises/editar/<int:pk>/', views.editar_pais, name='editar_pais'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/',views.crear_cliente,name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
]