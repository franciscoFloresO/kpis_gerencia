from django.urls import path
from . import views

urlpatterns = [
    # Debe recibir los dos parámetros que mencionamos en el selector
    path('redireccionar/<str:tipo>/', views.redireccionar_carga, name='redireccionar_carga'),
    path('cargar/<int:id_cliente>/<int:id_pais>/', views.cargar_operacion, name='cargar_operacion'),
    path('carga-contractual/<int:id_cliente>/<int:id_pais>/',views.cargar_contractual,name='cargar_contractual'),
    path('operacion/editar/<int:pk>/', views.editar_operacion, name='editar_operacion'),
    path('contractual/editar/<int:pk>/', views.editar_contractual, name='editar_contractual'),
    path('contractual/historial/', views.lista_contractual, name='lista_contractual'),
    path('operaciones/', views.lista_operaciones, name='lista_operaciones'),
]