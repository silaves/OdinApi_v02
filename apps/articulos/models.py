from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.autenticacion.models import Usuario
from apps.empresa.models import Empresa
from .validators import *

class Tienda(models.Model):
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=255)
    hora_inicio = models.TimeField(default='09:00:00',blank=True)
    hora_fin = models.TimeField(default='15:00:00',blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)

    def propietario(self):
        return self.empresa.empresario

    class Meta:
        db_table = 'TIENDA'
        verbose_name = _('tienda')
        verbose_name_plural = _('tiendas')
    
    def __str__(self):
        return self.id


class FotoTienda(models.Model):
    foto = models.ImageField(upload_to="articulos/tiendas/",blank=False,
        validators=[tamaño_del_archivo,],help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS)
    tienda = models.ForeignKey(Tienda, related_name='fotos',on_delete=models.CASCADE)

    class Meta:
        db_table = 'FOTO_TIENDA'
        verbose_name = _('foto tienda')
        verbose_name_plural = _('fotos tienda')
    
    def __str__(self):
        return self.id

class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(max_digits=7, decimal_places=1, blank=False)
    estado = models.BooleanField(default=True, blank=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.PROTECT)

    class Meta:
        db_table = 'ARTICULO'
        verbose_name = _('articulo')
        verbose_name_plural = _('articulos')
    
    def __str__(self):
        return self.id


class FotoArticulo(models.Model):
    foto = models.ImageField(upload_to="articulos/articulos/", default='articulos/articulos/no-img.jpg', null=True,blank=True,
        validators=[tamaño_del_archivo,],help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'FOTO_ARTICULO'
        verbose_name = _('foto articulo')
        verbose_name_plural = _('fotos articulos')
    
    def __str__(self):
        return self.id


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'FAVORITO'
        verbose_name = _('favorito')
        verbose_name_plural = _('favoritos')
    
    def __str__(self):
        return self.id


class CategoriaArticulo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'CATEGORIA_ARTICULO'
        verbose_name = _('categoria articulo')
        verbose_name_plural = _('categorias articulo')
    
    def __str__(self):
        return self.id


class SubCategoriaArticulo(models.Model):
    hijo = models.ForeignKey(CategoriaArticulo, on_delete=models.CASCADE, related_name='categoria_hijo')
    padre = models.ForeignKey(CategoriaArticulo, on_delete=models.CASCADE, related_name='sub_categorias')

    class Meta:
        unique_together =  (('hijo','padre'),)
        db_table = 'SUB_CATEGORIA_ARTICULO'
        verbose_name = _('sub categoria - articulo')
        verbose_name_plural = _('sub categorias - articulo')
    
    def __str__(self):
        return self.id


class Detalle(models.Model):
    label = models.CharField(max_length=30, blank=False)
    valor = models.CharField(max_length=50)
    estado = models.BooleanField(default=True, blank=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'DETALLE'
        verbose_name = _('detalle')
        verbose_name_plural = _('detalles')
    
    def __str__(self):
        return self.id


class SubDetalle(models.Model):
    valor = models.CharField(max_length=30, blank=False)
    estado = models.BooleanField(default=True, blank=True)
    detalle = models.ForeignKey(Detalle, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SUB_DETALLE'
        verbose_name = _('sub detalle')
        verbose_name_plural = _('sub detalles')
    
    def __str__(self):
        return self.id


class ChatArticulo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CHAT_ARTICULO'
        verbose_name = _('chat articulo')
        verbose_name_plural = _('chat articulos')
    
    def __str__(self):
        return self.id

class MensajeChat(models.Model):
    id_propietario = models.IntegerField(blank=False)
    mensaje = models.TextField(blank=False)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    chat = models.ForeignKey(ChatArticulo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'MENSAJE_CHAT'
        verbose_name = _('mensaje')
        verbose_name_plural = _('mensajes')
    
    def __str__(self):
        return self.id