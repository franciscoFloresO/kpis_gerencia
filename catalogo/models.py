from django.db import models


class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    nombre_pais = models.CharField(max_length=100, verbose_name="Nombre del País")
    codigo_pais = models.CharField(max_length=5, verbose_name="Código ISO (Ej: CL, PE)")
    estado_activo = models.BooleanField(default=True, verbose_name="¿Activo?")
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '[cat].[Pais]'
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self):
        return self.nombre_pais

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=150, verbose_name="Nombre del Cliente")
    vertical = models.CharField(max_length=100, verbose_name="Vertical de Negocio")
    estado_activo = models.BooleanField(default=True, verbose_name="¿Está Activo?")
    fecha_alta = models.DateField(verbose_name="Fecha de Alta")
    
    # Auditoría automática
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        # Esto es vital para que Django busque en el esquema 'cat'
        db_table = '[cat].[Cliente]'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre_cliente