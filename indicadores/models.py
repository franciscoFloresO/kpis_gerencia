from django.db import models
from catalogo.models import Pais, Cliente
from segmentacion.models import UsuarioApp
from django.core.validators import MinValueValidator, MaxValueValidator

class OperacionMensual(models.Model):
    id_operacion_mensual = models.BigAutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='id_pais')
    fecha_periodo = models.DateField()
    #HeadCount
    agentes_promedio = models.IntegerField()
    supervisores_promedio = models.IntegerField()
    backoffice_promedio = models.IntegerField()
    #Volumetria
    tickets_humano = models.IntegerField()
    hibridos_whatsapp_bi = models.IntegerField()
    porcentaje_digitalizacion = models.DecimalField(max_digits=5, decimal_places=2)
    tickets_digital = models.IntegerField()
    #Economico
    ingresos_totales_usd = models.DecimalField(max_digits=18, decimal_places=2)
    costos_totales_usd = models.DecimalField(max_digits=18, decimal_places=2)
    codigo_moneda = models.CharField(max_length=3, default='USD')
    #Automatico
    creado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, db_column='creado_por', related_name='operaciones_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    modificado_por = models.ForeignKey(UsuarioApp,on_delete=models.PROTECT,db_column='modificado_por',related_name='operaciones_modificadas',null=True,blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'kpi.OperacionMensual'
        unique_together = (('id_cliente', 'id_pais', 'fecha_periodo'),)


class OperacionMensualFS(models.Model):
    id_operacion_mensual = models.BigAutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='id_pais')
    fecha_periodo = models.DateField()
    
    # HeadCount
    agentes_promedio = models.IntegerField()
    supervisores_promedio = models.IntegerField()
    backoffice_promedio = models.IntegerField()
    
    # Volumetria
    tickets_humano = models.IntegerField()
    hibridos_whatsapp_bi = models.IntegerField()
    porcentaje_digitalizacion = models.DecimalField(max_digits=5, decimal_places=2)
    tickets_digital = models.IntegerField()
    
    # Economico
    ingresos_totales_usd = models.DecimalField(max_digits=18, decimal_places=2)
    costos_totales_usd = models.DecimalField(max_digits=18, decimal_places=2)
    codigo_moneda = models.CharField(max_length=3, default='USD')
    
    # Automatico
    creado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, db_column='creado_por', related_name='operaciones_fs_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    modificado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, db_column='modificado_por', related_name='operaciones_fs_modificados', null=True, blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'kpi.OperacionMensualFS'
        unique_together = (('id_cliente', 'id_pais', 'fecha_periodo'),)

class ContractualMensual(models.Model):
    id_contractual_mensual = models.BigAutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='id_pais')
    fecha_periodo = models.DateField()
    
    # Objetivos Porcentuales
    epa_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    fcr_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    sla_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    abandono_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Nuevos campos detectados en SQL
    asa_segundos_objetivo = models.IntegerField(null=True, blank=True)
    tmo_minutos_objetivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    acw_segundos_objetivo = models.IntegerField(null=True, blank=True)
    
    # Headcount objetivo
    agentes_objetivo = models.IntegerField(null=True, blank=True)
    supervisores_objetivo = models.IntegerField(null=True, blank=True)
    backoffice_objetivo = models.IntegerField(null=True, blank=True)
    
    descripcion_servicio = models.TextField()
    cobertura_horaria_multas = models.TextField(null=True, blank=True)

    # Auditoría
    creado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, db_column='creado_por', related_name='contractuales_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    modificado_por = models.ForeignKey(UsuarioApp,on_delete=models.PROTECT,db_column='modificado_por',related_name='contractuales_modificados',null=True,blank=True)
    fecha_contrato_modificacion = models.DateField(db_column='fecha_contrato_modificacion')

    class Meta:
        managed = False
        db_table = 'kpi.ContractualMensual'
        unique_together = (('id_cliente', 'id_pais', 'fecha_periodo'),)


class ContractualMensualFS(models.Model):
    id_contractual_mensual = models.BigAutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='id_pais')
    fecha_periodo = models.DateField()
    
    # Objetivos Porcentuales (Homologados a max_digits=5, decimal_places=2)
    epa_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    fcr_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    sla_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    abandono_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Objetivos de Tiempo y Dotación
    asa_segundos_objetivo = models.IntegerField(null=True, blank=True)
    tmo_segundos_objetivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    acw_segundos_objetivo = models.IntegerField(null=True, blank=True)
    
    # Headcount objetivo
    agentes_objetivo = models.IntegerField(null=True, blank=True)
    supervisores_objetivo = models.IntegerField(null=True, blank=True)
    backoffice_objetivo = models.IntegerField(null=True, blank=True)
    
    # Textos (Cambiados de CharField a TextField para calzar con el antiguo)
    descripcion_servicio = models.TextField()
    cobertura_horaria_multas = models.TextField(null=True, blank=True)

    # Auditoría
    creado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, db_column='creado_por', related_name='contractuales_fs_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    modificado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, db_column='modificado_por', related_name='contractuales_fs_modificados', null=True, blank=True)
    fecha_contrato_modificacion = models.DateField(db_column='fecha_contrato_modificacion')

    class Meta:
        managed = False
        db_table = 'kpi.ContractualMensualFS'
        unique_together = (('id_cliente', 'id_pais', 'fecha_periodo'),)

    def __str__(self):
        return f"CON: {self.id_cliente} - {self.id_pais} ({self.fecha_periodo})"
    



    

class Multa(models.Model):
    id_multa = models.AutoField(primary_key=True)
    
    # Relaciones maestras
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='id_pais')
    creado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT,db_column='creado_por')

    fecha_periodo = models.DateField()
    
    # Opciones para el CHECK constraint del Servicio
    SERVICIO_OPCIONES = [
        ('Field Service', 'Field Service'),
        ('Service Desk', 'Service Desk'),
    ]
    servicio = models.CharField(
        max_length=50, 
        choices=SERVICIO_OPCIONES,
        verbose_name="Tipo de Servicio"
    )
    
    monto_multa = models.DecimalField(max_digits=18, decimal_places=2)
    descripcion_multa = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        managed = False  # Respetamos el script manual de SQL
        db_table = '[kpi].[Multas]'
        verbose_name = "Multa"
        verbose_name_plural = "Multas"

    def __str__(self):
        return f"Multa {self.servicio}: {self.cliente} - {self.monto_multa}"