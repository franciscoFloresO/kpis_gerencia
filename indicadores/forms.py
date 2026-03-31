import datetime
from django import forms
from .models import OperacionMensual, ContractualMensual
# ... (tus otros imports)

class OperacionMensualForm(forms.ModelForm):
    # Campos virtuales que no existen en el modelo pero sí en el formulario
    MESES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    
    # Generamos una lista de años (año actual y 2 años hacia atrás/adelante)
    anio_actual = datetime.date.today().year
    ANIOS = [(str(y), str(y)) for y in range(anio_actual - 2, anio_actual + 3)]

    mes = forms.ChoiceField(choices=MESES, label="Mes del Periodo")
    anio = forms.ChoiceField(choices=ANIOS, label="Año del Periodo")

    class Meta:
        model = OperacionMensual
        # Quitamos 'fecha_periodo' de aquí porque usaremos los campos de arriba
        fields = [
            'id_pais', 'id_cliente', 'mes', 'anio',
            'agentes_promedio', 'supervisores_promedio', 'backoffice_promedio',
            'tickets_humano', 'hibridos_whatsapp_bi', 'porcentaje_digital_deflexion',
            'ingresos_totales_usd', 'costos_totales_usd', 'costo_ticket_usd', 'codigo_moneda'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OperacionMensualForm, self).__init__(*args, **kwargs)
        # ... (aquí mantienes tu lógica de filtrado de paises/clientes que ya hicimos)

    def clean(self):
        cleaned_data = super().clean()
        mes = int(cleaned_data.get('mes'))
        anio = int(cleaned_data.get('anio'))
        
        # Recomponemos la fecha al día 1 de ese mes
        # Esto es lo que se guardará en la columna 'fecha_periodo' de SQL Server
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

    class Meta:
        model = ContractualMensual
        fields = [
            'id_pais', 'id_cliente', 'mes', 'anio',
            'epa_objetivo', 'fcr_objetivo', 'sla_objetivo', 'abandono_objetivo',
            'asa_segundos_objetivo', 'tmo_minutos_objetivo', 'acw_segundos_objetivo',
            'agentes_objetivo', 'supervisores_objetivo', 'backoffice_objetivo',
            'descripcion_servicio', 'cobertura_horaria_multas'
        ]
        widgets = {
            'descripcion_servicio': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'cobertura_horaria_multas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos ocultos porque vienen de la URL
        self.fields['id_pais'].widget = forms.HiddenInput()
        self.fields['id_cliente'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        mes = cleaned_data.get('mes')
        anio = cleaned_data.get('anio')
        if mes and anio:
            cleaned_data['fecha_periodo'] = datetime.date(int(anio), int(mes), 1)
        return cleaned_data