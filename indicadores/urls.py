from django.urls import path
from . import views

urlpatterns = [
    # Debe recibir los dos parámetros que mencionamos en el selector
    path('cargar/<int:cliente_id>/<int:pais_id>/', views.cargar_operacion, name='cargar_operacion'),
]