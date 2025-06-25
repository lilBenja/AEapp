# app/serializers.py

from rest_framework import serializers
from .models import (
    Empresa,
    CargaFlexitank,
    CargaFlexirampla,
    ImagenCarga,
    Perfil,
)
from django.contrib.auth import get_user_model

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class TrabajoCargaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'empresa',
            'numero_flexi',
            'sello_flexi',
            'numero_naviera',
            'fecha_armado',
            'fierros_ref',
            'litros_cargados',
            'comentarios',
            'finalizar',
        ]

class CargaFlexitankSerializer(TrabajoCargaSerializer):
    class Meta(TrabajoCargaSerializer.Meta):
        model = CargaFlexitank
        fields = TrabajoCargaSerializer.Meta.fields + ['contenedor']

class CargaFlexiramplaSerializer(TrabajoCargaSerializer):
    class Meta(TrabajoCargaSerializer.Meta):
        model = CargaFlexirampla
        fields = TrabajoCargaSerializer.Meta.fields + ['patente_camion']

class ImagenCargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenCarga
        fields = ['id', 'imagen', 'nombre']

class PerfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Perfil
        fields = ['id', 'username', 'email', 'tipo_usuario']
