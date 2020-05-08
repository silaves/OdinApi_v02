from django.conf import settings
from rest_framework import serializers

from apps.empresa.models import Empresa
from apps.autenticacion.serializers import PerfilSerializer
from .models import *

# TIENDA

class CrearTienda_Serializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=50)
    descripcion = serializers.CharField(max_length=200)

    class Meta:
        model = Tienda
        fields = ['nombre','descripcion','telefono','direccion','hora_inicio','hora_fin']
    
    def validate_nombre(self, value):
        if Empresa.objects.filter(nombre=value).exists():
            raise serializers.ValidationError('El nombre ya esta en uso.')
        return value

class EditarEmpresa_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['nombre','descripcion']

class EditarTienda_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = ['telefono','direccion','hora_inicio','hora_fin']

class VerFotoTienda_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FotoTienda
        fields = ['id','foto']

class VerTienda_Serializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    descripcion = serializers.SerializerMethodField()
    propietario = PerfilSerializer()
    fotos = VerFotoTienda_Serializer(many=True,read_only=True)

    def get_nombre(self, obj):
        return obj.empresa.nombre
    
    def get_descripcion(self, obj):
        return obj.empresa.descripcion

    class Meta:
        model = Tienda
        fields = ['nombre','descripcion','telefono','direccion','hora_inicio','hora_fin','propietario','fotos']


class AgregarFotoTienda_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FotoTienda
        fields = ['foto','tienda']


# CATEGORIAS

# class CrearCategoria_Serializer(serializers.ModelSerializer):
#     categoria_padre = serializers.IntegerField(required=False, min_value=1)

#     class Meta:
#         model = CategoriaArticulo
#         fields = ['nombre','categoria_padre']
    
#     def validate_categoria_padre(self, value):
#         if not CategoriaArticulo.objects.filter(pk=value).exists():
#             raise ValidationError('No existe la categoria padre')
#         return value


class VerCategoriaArticulo_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaArticulo
        fields = '__all__'


class VerSubCategoriaArticulo_Serializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    # hijo = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()
    codigo = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    sub_categorias = serializers.SerializerMethodField()

    class Meta:
        model = SubCategoriaArticulo
        fields = ['id','codigo','nombre','estado','sub_categorias']
    
    def get_id(self, obj):
        try:
            value = obj.hijo.id
            return value
        except:
            return 0
    
    def get_nombre(self, obj):
        try:
            value = obj.hijo.nombre
            return value
        except:
            return None
    
    def get_codigo(self, obj):
        try:
            value = obj.hijo.codigo
            return value
        except:
            return None
    
    def get_estado(self, obj):
        try:
            value = obj.hijo.estado
            return value
        except:
            return None
    
    def get_sub_categorias(self, obj):
        try:
            _estado = self.context['_estado']
            value = obj.hijo.id
            if _estado == 'A':
                query = SubCategoriaArticulo.objects.filter(padre__id=value,hijo__estado=True)
            else:
                query = SubCategoriaArticulo.objects.filter(padre__id=value)
            return VerSubCategoriaArticulo_Serializer(query, many=True, context={'_estado':_estado}).data
        except:
            return None

class VerCategoriaHijosArticulo_Serializer(serializers.ModelSerializer):
    sub_categorias = serializers.SerializerMethodField('get_sub_categorias')

    class Meta:
        model = CategoriaArticulo
        fields = ['id','codigo','nombre','estado','sub_categorias']

    def get_sub_categorias(self,obj):
        _estado = self.context['_estado']
        if _estado == 'A':
            cate = SubCategoriaArticulo.objects.filter(padre__id=obj.id, hijo__estado=True)
        else:
            cate = SubCategoriaArticulo.objects.filter(padre__id=obj.id)
        
        ss = VerSubCategoriaArticulo_Serializer(instance=cate, many=True, context={'_estado':_estado})
        return ss.data

# ARTICULOS

class DetalleArticulo_Serializer(serializers.Serializer):
    detalles = serializers.CharField(max_length=100, required=True)

class CrearArticulo_Serializer(serializers.ModelSerializer):
    # detalles = DetalleArticulo_Serializer(many=True)
    detalles = serializers.ListField(
        required=True,
        # child = serializers.RegexField('^[a-zA-Z\u00C0-\u00FF]*$',max_length=10)
        child = serializers.CharField(max_length=255)
    )

    class Meta:
        model = Articulo
        fields = ['nombre','descripcion','precio','tienda','detalles']
    
    def validated_tienda(self, value):
        if value.empresa.empresario.id != self.context['id_usuario']:
            raise ValidationError('Usted no es propietario de la tienda')
        return value
    
    def validated_detalles(slef, value):
        detalle = value.split(':')
        label = detalle[0]
