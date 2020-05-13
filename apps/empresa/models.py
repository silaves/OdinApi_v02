from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.autenticacion.models import Usuario, Ciudad
from .validators import *
# Create your models here.

class CategoriaEmpresa(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    estado = models.BooleanField(default=True)
    # sub_categoria = models.IntegerField()

    class Meta:
        db_table = 'CATEGORIA_EMPRESA'
        verbose_name = _('categoria_empresa')
        verbose_name_plural = _('Categorias de una Empresa')
    
    def __str__(self):
        return self.nombre



class Empresa(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    empresario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaEmpresa, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True, blank=True)
    
    class Meta:
        db_table = 'EMPRESA'
        verbose_name = _('empresa')
        verbose_name_plural = _('empresas')
    
    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(_('Zona'),max_length=20)
    telefono = models.IntegerField()
    ubicacion = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=255)
    hora_inicio = models.TimeField(default='15:00:00',blank=True)
    hora_fin = models.TimeField(default='15:00:00',blank=True)
    disponible = models.BooleanField(default=False, blank=True)
    estado = models.BooleanField(default=True, blank=True)
    foto = models.ImageField(upload_to="sucursal/", default='sucursal/no-img.jpg', null=True, blank=True,
                             validators=[
                                 tamaño_del_archivo,
                             ],
                             help_text='El tamaño maximo para las fotos es %s Megas' % settings.MAXIMO_TAM_ARCHIVOS
                             )
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad,blank=True,null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'SUCURSAL'
        verbose_name = _('sucursal')
        verbose_name_plural = _('sucursales')
    
    def __str__(self):
        return self.nombre+' - '+self.empresa.nombre


class ProductoFinal(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(max_digits=7, decimal_places=1, blank=False)
    estado = models.BooleanField(default=True, blank=True)
    foto = models.ImageField(upload_to='productos/', default = 'productos/no-img.jpg', blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)

    class Meta:
        db_table = 'PRODUCTO_FINAL'
        verbose_name = _('producto_final')
        verbose_name_plural = _('productos_final')
    
    def __str__(self):
        return self.nombre

class Combo(models.Model):
    combo = models.ForeignKey(ProductoFinal, on_delete=models.PROTECT, related_name='combo')
    producto = models.ForeignKey(ProductoFinal, on_delete=models.PROTECT, related_name='producto')
    cantidad = models.PositiveSmallIntegerField(default=1, validators=[cantidad_min_value,cantidad_max_value])

    def clean(self):
        print('RATAMON')
        if self.combo.sucursal.id != self.producto.sucursal.id:
            raise ValidationError({'producto':'el producto es una mierda'})

    def save(self, *args, **kwargs):
        print('RATAS RATAS RATAS')
        super(Combo,self).save(*args, **kwargs)

    class Meta:
        unique_together =  (('combo','producto'),)
        db_table = 'COMBO'
        verbose_name = _('combo')
        verbose_name_plural = _('combos')
    
    def __str__(self):
        return self.producto


class Pedido(models.Model):
    total = models.DecimalField(max_digits=7, decimal_places=1, blank=False)
    cliente = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, default='N',choices=(
		('A','Activo'),('E', 'En Curso'),('F', 'Finalizado'),('C', 'Cancelado')
	))
    ubicacion = models.CharField(_('Direccion'), max_length=50, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    repartidor = models.ForeignKey(Usuario,blank=True,null=True,related_name='repartidor', on_delete=models.CASCADE)

    class Meta:
        db_table = 'PEDIDO'
        verbose_name = _('pedido')
        verbose_name_plural = _('pedidos')
    
    def __str__(self):
        return self.cliente.nombres


class PedidoProductoFinal(models.Model):
    cantidad = models.PositiveSmallIntegerField(default=1, validators=[cantidad_min_value,cantidad_max_value])
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    producto_final = models.ForeignKey(ProductoFinal, on_delete=models.PROTECT)

    class Meta:
        db_table = 'PEDIDO_PRODUCTO'
        verbose_name = _('pedido_producto')
        verbose_name_plural = _('pedido_productos')
    
    def __str__(self):
        return self.id


class Chat_Pedido(models.Model):
    ci = models.CharField(max_length=14)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)

    class Meta:
        db_table = 'CHAT_PEDIDO'
        verbose_name = _('chat_pedido')
        verbose_name_plural = _('chat_pedidos')
    
    def __str__(self):
        return self.id