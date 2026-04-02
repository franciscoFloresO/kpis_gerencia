import datetime
from django import forms
from .models import OperacionMensual, ContractualMensual
from django.core.validators import MinValueValidator, MaxValueValidator

class OperacionMensualForm(forms.ModelForm):

    MESES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]

    anio_actual = datetime.date.today().year
    ANIOS = [(str(y), str(y)) for y in range(anio_actual - 2, anio_actual + 3)]

    mes = forms.ChoiceField(choices=MESES, label="Mes del Periodo")
    anio = forms.ChoiceField(choices=ANIOS, label="Año del Periodo")

    porcentaje_digitalizacion = forms.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        label="Porcentaje Digitalización"
    )

    class Meta:
        model = OperacionMensual

        fields = [
            'id_pais', 'id_cliente', 'mes', 'anio',
            'agentes_promedio', 'supervisores_promedio', 'backoffice_promedio',
            'tickets_humano', 'hibridos_whatsapp_bi', 'porcentaje_digitalizacion', 'tickets_digital',
            'ingresos_totales_usd', 'costos_totales_usd', 'costo_ticket_usd', 'codigo_moneda'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OperacionMensualForm, self).__init__(*args, **kwargs)

        self.fields['id_pais'].widget = forms.HiddenInput()
        self.fields['id_cliente'].widget = forms.HiddenInput()
        self.fields['codigo_moneda'].widget = forms.HiddenInput()
        
        self.fields['codigo_moneda'].initial = 'USD'
        self.fields['codigo_moneda'].required = False

        if self.instance and self.instance.pk:
            
            self.fields['mes'].disabled = True
            self.fields['anio'].disabled = True
            self.fields['id_pais'].disabled = True
            self.fields['id_cliente'].disabled = True
            self.fields['codigo_moneda'].disabled = False

            self.fields['mes'].required = False
            self.fields['anio'].required = False



    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.pk:
            mes = self.instance.fecha_periodo.month
            anio = self.instance.fecha_periodo.year
            cliente = self.instance.id_cliente
            pais = self.instance.id_pais
        else:
            mes = int(cleaned_data.get('mes'))
            anio = int(cleaned_data.get('anio'))
            cliente = cleaned_data.get('id_cliente')
            pais = cleaned_data.get('id_pais')

        if mes and anio and cliente and pais:
            fecha_validar = datetime.date(int(anio), int(mes), 1)

            existe = OperacionMensual.objects.filter(
                id_cliente=cliente,
                id_pais=pais,
                fecha_periodo=fecha_validar
            )
        if self.instance.pk:
            existe = existe.exclude(pk=self.instance.pk)
        if existe.exists():
            raise forms.ValidationError(
                f"Atención: ya existe registro para {cliente}"
                f"en {pais} correspondiente para {mes}/{anio}"
            )
        cleaned_data['fecha_periodo'] = datetime.date(anio, mes, 1)
        return cleaned_data
    
class ContractualMensualForm(forms.ModelForm):
    MESES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    anio_actual = datetime.date.today().year
    ANIOS = [(str(y), str(y)) for y in range(anio_actual - 2, anio_actual + 3)]

    mes = forms.ChoiceField(choices=MESES, label="Mes del Periodo")
    anio = forms.ChoiceField(choices=ANIOS, label="Año del Periodo")

    epa_objetivo = forms.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        label="EPA Objetivo (%)"
    )
    fcr_objetivo = forms.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        label="FCR Objetivo (%)"
    )
    sla_objetivo = forms.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        label="SLA Objetivo (%)"
    )
    abandono_objetivo = forms.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        label="Abandono Máximo (%)"
    )

    class Meta:
        model = ContractualMensual
        fields = [
            'id_pais', 'id_cliente', 'mes', 'anio',
            'epa_objetivo', 'fcr_objetivo', 'sla_objetivo', 'abandono_objetivo',
            'asa_segundos_objetivo', 'tmo_minutos_objetivo', 'acw_segundos_objetivo',
            'agentes_objetivo', 'supervisores_objetivo', 'backoffice_objetivo',
            'descripcion_servicio', 'cobertura_horaria_multas'
        ]

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario por si se pasa desde la vista
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Ocultamos los campos de relación
        self.fields['id_pais'].widget = forms.HiddenInput()
        self.fields['id_cliente'].widget = forms.HiddenInput()

        # --- Lógica de Edición ---
        if self.instance and self.instance.pk:
            # Bloqueamos los campos de identidad
            self.fields['mes'].disabled = True
            self.fields['anio'].disabled = True
            self.fields['id_pais'].disabled = True
            self.fields['id_cliente'].disabled = True
            
            # Evitamos que Django los exija en el POST (ya que viajan como disabled)
            self.fields['mes'].required = False
            self.fields['anio'].required = False

        # Validadores de valores mínimos
        campos_min_cero = [
            'asa_segundos_objetivo', 'tmo_minutos_objetivo', 
            'acw_segundos_objetivo', 'agentes_objetivo', 
            'supervisores_objetivo', 'backoffice_objetivo'
        ]
        for campo in campos_min_cero:
            if campo in self.fields:
                self.fields[campo].validators.append(MinValueValidator(0))

    def clean(self):
        cleaned_data = super().clean()
        
        # Recuperamos el periodo según sea creación o edición
        if self.instance and self.instance.pk:
            mes = self.instance.fecha_periodo.month
            anio = self.instance.fecha_periodo.year
        else:
            mes = cleaned_data.get('mes')
            anio = cleaned_data.get('anio')

        if mes and anio:
            cleaned_data['fecha_periodo'] = datetime.date(int(anio), int(mes), 1)
            
        return cleaned_data