from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'tipo_usuario']
    list_filter = ['tipo_usuario']
    search_fields = ['user__username', 'user__email']
