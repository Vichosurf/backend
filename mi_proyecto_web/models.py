from pathlib import Path

from django.conf import settings
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=160)
    categoria = models.CharField(max_length=80)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    imagen = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nombre

    @property
    def imagen_visible(self):
        if self.imagen.startswith('http'):
            return self.imagen
        imagen_path = Path(settings.BASE_DIR) / 'mi_proyecto_web' / 'static' / self.imagen
        if self.imagen and imagen_path.exists():
            return self.imagen
        return 'imagenes/producto-placeholder.svg'