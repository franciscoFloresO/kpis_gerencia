from django import forms
from .models import Cliente, Pais

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_cliente', 'vertical', 'estado_activo', 'fecha_alta']
        
        widgets = {
            'fecha_alta': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date', 'class': 'form-control'}
            ),
            'nombre_cliente': forms.TextInput(attrs={'placeholder': 'Nombre Cliente', 'class': 'form-control'}),
            'vertical': forms.TextInput(attrs={'placeholder': 'Nombre Vertical', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['fecha_alta'].disabled = True
            self.fields['fecha_alta'].required = False


class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['nombre_pais', 'codigo_pais', 'estado_activo']
        widgets = {
            'nombre_pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Chile'}),
            'codigo_pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: CL'}),
        }