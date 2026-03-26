from django.db import models

class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    nombre_pais = models.CharField(max_length=100, unique=True)
    codigo_pais = models.CharField(max_length=10, unique=True, null=True, blank=True)
    estado_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False  # Importante: Django no intentará crear/modificar la tabla
        db_table = 'cat.Pais' # Mapeo al esquema 'cat'

    def __str__(self):
        return self.nombre_pais

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=150, unique=True)
    vertical = models.CharField(max_length=100, null=True, blank=True)
    estado_activo = models.BooleanField(default=True)
    fecha_alta = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'cat.Cliente'

    def __str__(self):
        return self.nombre_cliente