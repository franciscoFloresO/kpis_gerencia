from django.urls import path
from . import views

urlpatterns = [
    # Debe recibir los dos parámetros que mencionamos en el selector
    path('redireccionar/<str:tipo>/', views.redireccionar_carga, name='redireccionar_carga'),
    path('cargar/sd/<int:id_cliente>/<int:id_pais>/', views.cargar_operacion, name='cargar_operacion'),
    path('cargar/fs/<int:id_cliente>/<int:id_pais>/', views.cargar_operacion_fs, name='cargar_operacion_fs'),

    path('carga-contractual/sd/<int:id_cliente>/<int:id_pais>/', views.cargar_contractual, name='cargar_contractual'),
    path('carga-contractual/fs/<int:id_cliente>/<int:id_pais>/', views.cargar_contractual_fs, name='cargar_contractual_fs'),

    path('operacion/editar/<int:pk>/', views.editar_operacion, name='editar_operacion'),
    path('contractual/editar/<int:pk>/', views.editar_contractual, name='editar_contractual'),
    path('contractual/historial/', views.lista_contractual, name='lista_contractual'),
    path('operaciones/', views.lista_operaciones, name='lista_operaciones'),
    path('contractual/historial-fs/', views.lista_contractual_fs, name='lista_contractual_fs'),
    path('operaciones-fs/', views.lista_operaciones_fs, name='lista_operaciones_fs'),

    path('operacion/editar-fs/<int:pk>/', views.editar_operacion_fs, name='editar_operacion_fs'),
    path('contractual/editar-fs/<int:pk>/', views.editar_contractual_fs, name='editar_contractual_fs'),

    path('multas/', views.gestion_multas, name='gestion_multas'),
    path('multas/cargar/<int:id_cliente>/<int:id_pais>/', views.cargar_multa, name='cargar_multa'),
    path('multas/editar/<int:pk>', views.editar_multa, name='editar_multa'),
]