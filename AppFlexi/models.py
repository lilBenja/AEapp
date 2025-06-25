from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone # Asegúrate de que esta función esté definida en utils.py
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre 


class TrabajoCarga(models.Model):
    EMPRESAS_CHOICES = [
        ("Tiba", "Tiba"),
        ("Manuport", "Manuport"),
        ("Hillebrand", "Hillebrand"),
        ("DHL", "DHL"),
        ("Belog", "Belog"),
        ("Cacsa", "Cacsa"),
        ("Otra", "Otra empresa"),
    ]

    empresa = models.CharField(max_length=50, choices=EMPRESAS_CHOICES, default="Otra")
    numero_flexi = models.CharField(max_length=50, null=True, blank=True)
    sello_flexi = models.CharField(max_length=50, null=True, blank=True)
    numero_naviera = models.CharField(max_length=50, null=True, blank=True)
    fecha_armado = models.DateTimeField(default=timezone.now)
    fierros_ref = models.CharField(max_length=50, null=True, blank=True)  
    litros_cargados = models.FloatField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    finalizar = models.BooleanField(default=False)

    class Meta:
        abstract = True  # No se crea una tabla para esta clase

class CargaFlexitank(TrabajoCarga):
    contenedor = models.CharField(max_length=50)  #  Solo los flexitanks tienen contenedor

    def __str__(self):
        return f"Flexitank - {self.empresa} ({self.contenedor})"

class CargaFlexirampla(TrabajoCarga):
    patente_camion = models.CharField(max_length=20)  #  Solo las flexirampla tienen patente

    def __str__(self):
        return f"Flexirampla - {self.empresa} ({self.patente_camion})"


class ImagenCarga(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')
    nombre = models.CharField(max_length=100, blank=True)

    carga_flexitank = models.ForeignKey(
        'CargaFlexitank',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )

    carga_flexirampla = models.ForeignKey(
        'CargaFlexirampla',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )

    def save(self, *args, **kwargs):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile

        img = Image.open(self.imagen)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        max_width = 1280
        if img.width > max_width:
            height = int((max_width / img.width) * img.height)
            img = img.resize((max_width, height), Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=80)

        self.imagen.save(
            self.imagen.name,
            ContentFile(buffer.getvalue()),
            save=False
        )

        super().save(*args, **kwargs)

    
class Perfil(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('SUPERVISOR', 'Supervisor'),
        ('TRABAJADOR', 'Trabajador'),
        ('EMPRESA', 'Empresa'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.get_tipo_usuario_display()})"