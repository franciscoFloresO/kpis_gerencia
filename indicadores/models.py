from django.db import models
from catalogo.models import Pais, Cliente
from segmentacion.models import UsuarioApp

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
    porcentaje_digital_deflexion = models.DecimalField(max_digits=5, decimal_places=2)
    #Economico
    ingresos_totales_usd = models.DecimalField(max_digits=18, decimal_places=2)
    costos_totales_usd = models.DecimalField(max_digits=18, decimal_places=2)
    costo_ticket_usd = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    codigo_moneda = models.CharField(max_length=3, default='USD')
    #Automatico
    creado_por = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, db_column='creado_por', related_name='operaciones_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'kpi.OperacionMensual'
        unique_together = (('id_cliente', 'id_pais', 'fecha_periodo'),)

class ContractualMensual(models.Model):
    id_contractual_mensual = models.BigAutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='id_pais')
    fecha_periodo = models.DateField()
    
    epa_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    fcr_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    sla_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    abandono_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
    
    descripcion_servicio = models.TextField()

    class Meta:
        managed = False
        db_table = 'kpi.ContractualMensual'
        unique_together = (('id_cliente', 'id_pais', 'fecha_periodo'),)