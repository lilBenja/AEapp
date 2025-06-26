from django.contrib import admin
from .models import Empresa, CargaFlexitank, CargaFlexirampla, ImagenCarga, Perfil

# Para mostrar vista previa de imagen
from django.utils.html import format_html
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'tipo_usuario']
    list_filter = ['tipo_usuario']
    search_fields = ['user__username', 'user__email']

from django.contrib import admin
from .models import Empresa, CargaFlexitank, CargaFlexirampla, ImagenCarga, Perfil

# Para mostrar vista previa de imagen
from django.utils.html import format_html

class ImagenCargaInline(admin.TabularInline):
    model = ImagenCarga
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="150" />', obj.imagen.url)
        return "No hay imagen"
    imagen_preview.short_description = "Vista previa"

@admin.register(CargaFlexitank)
class CargaFlexitankAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'contenedor', 'numero_flexi', 'fecha_armado', 'finalizar']
    search_fields = ['empresa', 'contenedor', 'numero_flexi']
    inlines = [ImagenCargaInline]

@admin.register(CargaFlexirampla)
class CargaFlexiramplaAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'patente_camion', 'numero_flexi', 'fecha_armado', 'finalizar']
    search_fields = ['empresa', 'patente_camion', 'numero_flexi']
    inlines = [ImagenCargaInline]

@admin.register(ImagenCarga)
class ImagenCargaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'carga_flexitank', 'carga_flexirampla', 'imagen_preview']
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="150" />', obj.imagen.url)
        return "No hay imagen"
    imagen_preview.short_description = "Vista previa"

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
