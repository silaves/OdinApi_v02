from decimal import Decimal
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.autenticacion.models import Usuario
from .models import Empresa, Sucursal, Combo, ProductoFinal, CategoriaEmpresa, Pedido, PedidoProductoFinal
from apps.autenticacion.serializers import PerfilSerializer

class CategoriaEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaEmpresa
        fields = ['id','nombre','estado']


class EmpresaSerializer(serializers.ModelSerializer):
    categoria = CategoriaEmpresaSerializer()
    
    class Meta:
        model = Empresa
        fields = ['id','nombre','descripcion','empresario','categoria']
    
    def create(self, validate_data):
        return Empresa.objects.create(**validate_data)
    
    def validate_nombre(self, value):
        if len(value) > 40:
            raise forms.ValidationError('El nombre es muy largo')
        return value
    
    def validate_descripcion(self, value):
        if len(value) > 500:
            raise forms.ValidationError('la descripcion es muy larga')
        return value


class EmpresaEditarSerializer(serializers.ModelSerializer):
    categoria = CategoriaEmpresaSerializer(read_only=True)
    
    class Meta:
        model = Empresa
        fields = ['id','nombre','descripcion','categoria']
    
    def validate_nombre(self, value):
        if len(value) > 40:
            raise forms.ValidationError('El nombre es muy largo')
        return value
    
    def validate_descripcion(self, value):
        if len(value) > 500:
            raise forms.ValidationError('la descripcion es muy larga')
        return value


class SucursalSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()

    class Meta:
        model = Sucursal
        fields = ['id','nombre','disponible','estado','telefono','direccion','foto','empresa','hora_inicio','hora_fin']
    


class SucursalEditarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['nombre','telefono','direccion','foto','hora_inicio','hora_fin','estado']


class ProductoFinalSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = ProductoFinal
        fields = ['id','nombre','descripcion','precio','sucursal','foto']
    
    # def create(self, validate_data):
    #     return Producto.objects.create(**validate_data)


class ProductoFinalEditarSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = ProductoFinal
        fields = ['nombre','descripcion','precio','estado','foto']

class ProductoFinalVerSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = ProductoFinal
        fields = ['id','nombre','descripcion','precio','estado','sucursal','foto']



# Combo


#crear combo

class CrearComboSerializer(serializers.ModelSerializer):
    combo = serializers.ListField(
        child = serializers.RegexField('^\d{1,8}[-]\d{1,2}?$',max_length=10)
    )

    class Meta:
        model = ProductoFinal
        fields = ['nombre','descripcion','precio','sucursal','foto','combo']
        
    def validate(self, data):
        index = 0
        ides = []
        for x in data['combo']:
            line = x.split('-')
            ides.append(int(line[0]))
            if line[0] == '0' or line[1] == '0':
                raise serializers.ValidationError({'combo':{str(index):['Los valores no pueden ser negativos o ceros.']}})
            try:
                producto = ProductoFinal.objects.get(pk=int(line[0]))
            except:
                raise serializers.ValidationError({'combo':{str(index):['No existe el producto.']}})
            if producto.sucursal.id != data['sucursal'].id:
                raise serializers.ValidationError({'combo':{str(index):['La sucursal del producto no esta asociada a la del padre.']}})
            index+=1
        while len(ides) > 0:
            try:
                value = ides.pop()
            except:
                value = -1
            if value in ides:
                raise serializers.ValidationError({'combo':['No debe haber productos repetidos en el combo']})
        return data
    
    def create(self, validated_data):
        data = validated_data.pop('combo')
        return ProductoFinal.objects.create(**validated_data)


# editar combo
class EditarComboSerializer(serializers.ModelSerializer):
    combo = serializers.ListField(
        required=False,
        child = serializers.RegexField('^\d{1,8}[-]\d{1,2}?$',max_length=10)
    )
    nombre = serializers.CharField(required=False,max_length=50)
    precio = serializers.DecimalField(max_digits=7, decimal_places=1, required=False)

    class Meta:
        model = ProductoFinal
        fields = ['nombre','descripcion','precio','foto','combo']
    
    def validate(self, data):
        index = 0
        ides = []
        theris_pr = True
        try:
            data['combo']
        except:
            theris_pr = False
        
        if theris_pr:
            for x in data['combo']:
                line = x.split('-')
                ides.append(int(line[0]))
                if line[0] == '0' or line[1] == '0':
                    raise serializers.ValidationError({'combo':{str(index):['Los valores no pueden ser negativos o ceros.']}})
                try:
                    producto = ProductoFinal.objects.get(pk=int(line[0]))
                except:
                    raise serializers.ValidationError({'combo':{str(index):['No existe el producto.']}})
                if producto.sucursal.id != self.instance.sucursal.id:
                    raise serializers.ValidationError({'combo':{str(index):['La sucursal del producto no esta asociada a la del padre.']}})
                index+=1
            while len(ides) > 0:
                try:
                    value = ides.pop()
                except:
                    value = -1
                if value in ides:
                    raise serializers.ValidationError({'combo':['No debe haber productos repetidos en el combo']})
        return data
    
    def create(self, validated_data):
        data = validated_data.pop('combo')
        return ProductoFinal.objects.create(**validated_data)


# ver combo
class VerProductoFinalSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)
    combo = serializers.SerializerMethodField('cargar_pro')

    class Meta:
        model = ProductoFinal
        fields = ['id','nombre','descripcion','precio','estado','sucursal','foto','combo']
    
    def cargar_pro(self, obj):
        if obj.id:
            pros = ProductoFinal.objects.filter(id__in=Combo.objects.filter(combo_id=obj.id).values('producto'))
            if len(pros) > 0:
                return ProSerializer(pros, many=True).data
            else:
                return False
        else:
            return None


class ComboSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = ProductoFinal
        fields = ['id','nombre','descripcion','precio','sucursal','foto', 'productos']



class ResponseProducto(serializers.ModelSerializer):
     class Meta:
         model = ProductoFinal
         fields = ['id']

class ResponseCombo(serializers.ModelSerializer):
    foto = serializers.ImageField(use_url=True, required=False, allow_null=True)
    productos = ResponseProducto(many=True)

    class Meta:
        model = ProductoFinal
        fields = ('nombre','descripcion','precio','sucursal', 'productos','foto',)

class ResponseComboEditar(serializers.ModelSerializer):
    foto = serializers.ImageField(use_url=True, required=False, allow_null=True)
    productos = ResponseProducto(required=False,many=True)
    nombre = serializers.CharField(required=False)
    precio = serializers.DecimalField(max_digits=7, decimal_places=1,required=False)

    class Meta:
        model = ProductoFinal
        fields = ('nombre','descripcion','precio','estado', 'productos','foto',)



        
# class ComboSerializer(serializers.ModelSerializer):
#     foto = serializers.ImageField(required=True,max_length=None, use_url=True)

#     class Meta:
#         model = Combo
#         fields = ['id','nombre','descripcion','precio','estado','foto']
    
#     # def create(self, validate_data):
#     #     return Producto.objects.create(**validate_data)


class ComboEditarSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=True, use_url=True)

    class Meta:
        model = ProductoFinal
        fields = ['nombre','descripcion','precio','estado','foto']



# Serializador para crear pedidos

class ProductoP_Serializer(serializers.Serializer):
    id = serializers.IntegerField()

class ComboP_Serializer(serializers.Serializer):
    id = serializers.IntegerField()

class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoP_Serializer(many=True)
    combos = ComboP_Serializer(many=True)
    sucursal = serializers.IntegerField()

    class Meta:
        model = Pedido
        fields = ('sucursal','cliente','productos','combos')
    
    # def validate_sucursal(self, value):
    #     if not Sucursal.objects.filter(pk=value).exists():
    #         raise serializers.ValidationError("La sucursal no existe")
    #     return value
    
    # def validate_productos(self, value):
    #     for x in value:
    #         if not Producto.objects.filter(pk=x['id']).exists():
    #             raise serializers.ValidationError("El producto no existe")
    #     return value
    
    # def validate_combos(self, value):
    #     for x in value:
    #         if not Combo.objects.filter(pk=x['id']).exists():
    #             raise serializers.ValidationError("El combo no existe")
    #     return value
    
    # def create(self,validate_data):
    #     print(validate_data)
    #     sucursal = Sucursal.objects.get(pk=validate_data['sucursal'])
    #     total = Decimal(0.0)
    #     cliente = Usuario.objects.get(pk=validate_data['cliente'].id)
    #     obj = Pedido.objects.create(cliente=cliente, total=total)
    #     obj.save()
    #     # sumar precios de pructos y combos
    #     for x in validate_data['productos']:
    #         producto = Producto.objects.get(pk=x['id'])
    #         pp = PedidoProducto.objects.create(pedido=obj, producto=producto)
    #         total = total + producto.precio
    #     for x in validate_data['combos']:
    #         combo = Combo.objects.get(pk=x['id'])
    #         pc = PedidoCombo.objects.create(pedido=obj, combo=combo)
    #         total = total + combo.precio
    #     obj.total = total
    #     obj.save()
    #     return obj

class ps(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField('get_pro')
    # combos = ComboP_Serializer(many=True)
    # sucursal = serializers.IntegerField()
    class Meta:
        model = Pedido
        fields = ('sucursal','cliente','productos')

    def get_pro(self, obj):
        sucursales = Sucursal.objects.all()
        return SucursalSerializer(sucursales,many=True).data




# PARA OBTENER PEDIDOS - CLIENTE

class ProSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = ProductoFinal
        fields = ['id','nombre','descripcion','precio','estado','sucursal','foto']

class ProFinalSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)
    sucursal = SucursalSerializer()
    productos = serializers.SerializerMethodField('cargar_pro')

    class Meta:
        model = ProductoFinal
        fields = ['id','nombre','descripcion','precio','estado','sucursal','foto','productos']
    
    def cargar_pro(self, obj):
        if obj.id:
            try:
                combo = Combo.objects.get(pk=obj.id)
                pros = ProductoFinal.objects.filter(id__in=ComboProducto.objects.filter(combo=combo).values('producto'))
                return ProSerializer(pros, many=True).data
            except Exception as e:
                pros = ProductoFinal.objects.get(pk=obj.id)
                return False
        else:
            return None

class PedidosCustomSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField('cargar_productos')

    class Meta:
        model = Pedido
        fields = ('id','sucursal','cliente','repartidor','estado','fecha','direccion','productos')
    
    def cargar_productos(self, obj):
        if obj.id:
            productos = ProductoFinal.objects.filter(id__in=PedidoProductoFinal.objects.filter(pedido=obj.id).values('producto_final'))
            return ProFinalSerializer(productos, many=True).data


# PARA OBTENER PEDIDOS - SUCURSAL

class ProFinalSucursalSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(max_length=None, use_url=True)
    combo = serializers.SerializerMethodField('cargar_pro')

    class Meta:
        model = ProductoFinal
        fields = ['id','nombre','descripcion','precio','estado','sucursal','foto','combo']
    
    def cargar_pro(self, obj):
        if obj.id:
            if len(Combo.objects.filter(combo__id=obj.id)) > 0:
                return True
            else:
                return False
        else:
            return None

class PedidosSucursalCustomSerializer(serializers.ModelSerializer):
    cliente = PerfilSerializer()
    productos = serializers.SerializerMethodField('cargar_productos')

    class Meta:
        model = Pedido
        fields = ('id','sucursal','cliente','repartidor','estado','fecha','direccion','productos','total')
    
    def cargar_productos(self, obj):
        if obj.id:
            productos = ProductoFinal.objects.filter(id__in=PedidoProductoFinal.objects.filter(pedido=obj.id).values('producto_final'))
            return ProFinalSucursalSerializer(productos, many=True).data



# serializadores para la documentacion.. no influyen en el logica del sistema.

class ResponseProductodID(serializers.ModelSerializer):
    id = serializers.IntegerField(label='id del producto')

    class Meta:
        model = ProductoFinal
        fields = ['id']
    
    def validate_id(self, value):
        try:
            obj = ProductoFinal.objects.get(pk=value)            
        except:
            raise serializers.ValidationError('El producto no existe')
        if obj.estado is False:
            raise serializers.ValidationError('El producto no esta disponible')
        return value


class ResponsePedidos(serializers.ModelSerializer):
    productos = ResponseProductodID(many=True)
    combos = ResponseProductodID(many=True)

    class Meta:
        model = Pedido
        fields = ('sucursal','cliente','productos','combos')


class ResponsePedidosEditar(serializers.ModelSerializer):
    productos = ResponseProductodID(many=True)
    combos = ResponseProductodID(many=True)

    class Meta:
        model = Pedido
        fields = ('productos','combos')

class ResponseTokenFirebase(serializers.Serializer):
    token_firebase = serializers.CharField(max_length=255, read_only=True)


# CREAR PEDDIDOS FINAL

class PedidoProductos(serializers.ModelSerializer):
    cantidad = serializers.IntegerField(required=True,max_value=99, min_value=1)

    class Meta:
        model = PedidoProductoFinal
        fields = ('cantidad','producto_final')

    def validate_producto_final(self, value):
        if value.estado == False:
            raise serializers.ValidationError('El producto esta inactivo')
        return value


class CrearPedidoSerializer(serializers.ModelSerializer):
    productos = PedidoProductos(required=True,many=True)

    class Meta:
        model = Pedido
        fields = ('sucursal','direccion','productos')
    
    def validate(self, data):
        for x in data['productos']:
            if x['producto_final'].sucursal.id != data['sucursal'].id:
                raise serializers.ValidationError({'productos':'Hay productos(s) que no pertenecen a la sucursal.'})
        return data

    def validate_productos(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('El pedido debe tener al menos 1 producto.')
        return value

#asd
class EditarPedidoSerializer(serializers.ModelSerializer):
    productos = PedidoProductos(required=False,many=True)

    class Meta:
        model = Pedido
        fields = ('direccion','productos')
    
    def validate(self, data):
        try:
            data['productos']
            is_productos = True
        except:
            is_productos = False
        if is_productos is True:
            for x in data['productos']:
                if x['producto_final'].sucursal.id != self.instance.sucursal.id:
                    raise serializers.ValidationError({'productos':'Hay productos(s) que no pertenecen a la sucursal.'})
        return data

    def validate_productos(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('El pedido debe tener al menos 1 producto.')
        return value


# Serializadores para pedido

# class CrearPedidoSerializer(serializers.ModelSerializer):
#     productos_finales = ResponseProductodID(many=True)

#     class Meta:
#         model = Pedido
#         fields = ('sucursal','direccion','productos_finales')
    
#     def validate(self, data):
#         for x in data['productos_finales']:
#             p = ProductoFinal.objects.get(pk=x['id'])
#             if p.sucursal.id != data['sucursal'].id:
#                 raise serializers.ValidationError('Algunos de los productos no pertenecen a la sucursal a la cual quiere hacer el pedido')
#         return data


# class EditarPedidoSerializer(serializers.ModelSerializer):
#     productos_finales = ResponseProductodID(many=True)

#     class Meta:
#         model = Pedido
#         fields = ('direccion','productos_finales',)
    
#     def validate(self, data):
#         for x in data['productos_finales']:
#             p = ProductoFinal.objects.get(pk=x['id'])
#             if p.sucursal.id != self.instance.sucursal.id:
#                 raise serializers.ValidationError('Algunos de los productos no pertenecen a la sucursal a la cual quiere hacer el pedido')
#         return data

class CambiarDisponibleSucursal_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['disponible']