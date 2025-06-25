from django import forms
from .models import CargaFlexitank, CargaFlexirampla
from django.contrib.auth.forms import UserCreationForm

EMPRESAS_PERMITIDAS = ["Tiba", "Manuport", "Hillebrand", "DHL", "Belog", "Cacsa"]

class MenuForm(forms.Form):
    OPCIONES = [
        ('carga', 'Carga'),
        ('trasvasije', 'Trasvasije'),
        ('inspeccion_contenedor', 'Inspección contenedor'),
        ('inspeccion_flexitank', 'Inspección flexitank'),
    ]
    
    opcion = forms.ChoiceField(choices=OPCIONES, widget=forms.Select, label="Seleccione una opción")

class CargaFlexitankForm(forms.ModelForm):
    class Meta:
        model = CargaFlexitank
        fields = "__all__"
        exclude = ['finalizar', 'comentarios']  # Excluimos el campo 'finalizar' del formulario

class CargaFlexiramplaForm(forms.ModelForm):
    class Meta:
        model = CargaFlexirampla
        fields = "__all__"
        exclude = ['finalizar', 'comentarios'] # Excluimos los campos 'finalizar' y 'comentarios' del formulario

