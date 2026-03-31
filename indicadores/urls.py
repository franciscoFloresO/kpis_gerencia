from django.urls import path
from . import views

urlpatterns = [
    # Debe recibir los dos parámetros que mencionamos en el selector
    path('redireccionar/<str:tipo>/', views.redireccionar_carga, name='redireccionar_carga'),
    path('cargar/<int:id_cliente>/<int:id_pais>/', views.cargar_operacion, name='cargar_operacion'),
    path('carga-contractual/<int:id_cliente>/<int:id_pais>/',views.cargar_contractual,name='cargar_contractual'),
]