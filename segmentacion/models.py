from django.db import models
from catalogo.models import Pais, Cliente

class UsuarioApp(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    usuario_login = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    nombre_completo = models.CharField(max_length=200)
    correo_corporativo = models.EmailField(max_length=200, unique=True)
    es_administrador_global = models.BooleanField(default=False)
    estado_activo = models.BooleanField(default=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(db_column='ultimo_acceso', null=True, blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True)

    fs = models.BooleanField(default=False, db_column='fs')
    sd = models.BooleanField(default=False, db_column='sd')

    # Propiedades de compatibilidad con Django
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return self.estado_activo

    class Meta:
        managed = False
        db_table = 'seg.UsuarioApp'

    def __str__(self):
        return f"{self.usuario_login} ({self.nombre_completo})"

class UsuarioClientePais(models.Model):
    id = models.AutoField(primary_key=True,db_column='id_usuario_cliente_pais')
    
    usuario = models.ForeignKey(UsuarioApp, on_delete=models.CASCADE, db_column='id_usuario')
    cliente = models.ForeignKey('catalogo.Cliente', on_delete=models.CASCADE, db_column='id_cliente')
    pais = models.ForeignKey('catalogo.Pais', on_delete=models.CASCADE, db_column='id_pais')
    
    estado_activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'seg.UsuarioClientePais'
        # Ajustamos el unique_together con los nuevos nombres
        unique_together = (('usuario', 'cliente', 'pais'),)