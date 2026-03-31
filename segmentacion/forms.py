from django import forms
from .models import UsuarioApp, Pais, Cliente, UsuarioClientePais
from django.contrib.auth.hashers import make_password

class UsuarioAppForm(forms.ModelForm):
    #Se especifican ambos inputs de password para poder trabajar la edición del usuario y que se pueda cambiar la contraseña
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Dejar en blanco para no cambiar'}),
        required=False, 
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'}),
        required=False,
        label="Confirmar Contraseña"
    )
    #Valores manuales a trabajar desde el models.py
    class Meta:
        model = UsuarioApp
        fields = [
            'usuario_login',
            'nombre_completo',
            'correo_corporativo',
            'password',
            'es_administrador_global',
            'estado_activo'
        ]
    #Listado para dar orden en el formulario del html    
    field_order = [
        'usuario_login', 
        'nombre_completo', 
        'correo_corporativo', 
        'password', 
        'password_confirm', 
        'es_administrador_global',
        'estado_activo'
    ]

    #Función para no aceptar cualquier tipo de correo y solo alguno de sonda.
    def clean_correo_corporativo(self):
        correo = self.cleaned_data.get('correo_corporativo').lower()
        dominios = ['@sonda.com', '@ext.sonda.com']

        if not any(correo.endswith(dom) for dom in dominios):
            raise forms.ValidationError('El correo debe pertenecer a @sonda.com o @ext.sonda.com')
        
        return correo

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if not self.instance.pk and not password:
            self.add_error('password', "La contraseña es obligatoria para usuarios nuevos.")

        if password and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
            
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        nueva_pwd = self.cleaned_data.get("password")
        
        if nueva_pwd:
            user.password = make_password(nueva_pwd)
        else:
            if self.instance.pk:
                user.password = UsuarioApp.objects.get(pk=self.instance.pk).password
        
        if commit:
            user.save()
        return user
    
class AsignacionForm(forms.ModelForm):
    class Meta:
        model = UsuarioClientePais
        fields = ['pais', 'cliente']

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario que pasaremos desde la vista
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pais = cleaned_data.get("pais")
        cliente = cleaned_data.get("cliente")

        # Validamos si ya existe la combinación para este usuario
        if self.usuario and pais and cliente:
            existe = UsuarioClientePais.objects.filter(
                usuario=self.usuario,
                pais=pais,
                cliente=cliente
            ).exists()
            
            if existe:
                raise forms.ValidationError(
                    f"Error: {pais} - {cliente} ya se encuentra asignado a este usuario."
                )
        
        return cleaned_data