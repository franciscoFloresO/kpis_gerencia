# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('selector/', views.selector_contexto, name='selector_contexto'),
    path('usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar(<int:id_usuario>/)', views.editar_usuario, name='editar_usuario'),
    path('lista_usuarios/',views.lista_usuarios,name='lista_usuarios'),
    path('home/', views.home, name='home'),
    path('usuarios/<int:id_usuario>/asignaciones', views.gestionar_asignaciones, name='gestionar_asignaciones'),
    path('asignaciones/eliminar/<int:id_asignaciones>/', views.eliminar_asignacion, name='eliminar_asignacion'),
]