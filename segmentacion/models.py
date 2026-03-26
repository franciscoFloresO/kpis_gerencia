from django.db import models
from catalogo.models import Pais, Cliente

class UsuarioApp(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    usuario_login = models.CharField(max_length=150, unique=True)
    nombre_completo = models.CharField(max_length=200)
    correo_corporativo = models.CharField(max_length=200, unique=True)
    es_administrador_global = models.BooleanField(default=False)
    estado_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'seg.UsuarioApp'

    def __str__(self):
        return self.nombre_completo

class UsuarioClientePais(models.Model):
    id_usuario_cliente_pais = models.AutoField(primary_key=True)
    # Relaciones entre apps
    id_usuario = models.ForeignKey(UsuarioApp, on_delete=models.CASCADE, db_column='id_usuario')
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='id_pais')
    estado_activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'seg.UsuarioClientePais'
        unique_together = (('id_usuario', 'id_cliente', 'id_pais'),)