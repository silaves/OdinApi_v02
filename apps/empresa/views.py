from typing import Dict, Any
import json
import jwt
import time as ti
import timeit
from datetime import date, datetime, time
from drf_yasg.utils import swagger_auto_schema
from urllib.error import HTTPError
from datetime import timedelta
from decimal import Decimal
from django.utils.timezone import make_aware
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from requests.exceptions import HTTPError

from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework import permissions, exceptions
from rest_framework import generics, permissions, status, views
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, renderer_classes, parser_classes, action

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden

from apps.autenticacion.views import permission_required
from .models import Empresa, Sucursal, ProductoFinal, Combo, CategoriaEmpresa, Pedido,PedidoProductoFinal
from .serializers import (EmpresaSerializer, EmpresaEditarSerializer, SucursalSerializer, ProductoFinalSerializer, ProductoFinalEditarSerializer,
    ProductoFinalVerSerializer, ps,PedidosCustomSerializer,PedidosSucursalCustomSerializer, ProFinalSucursalSerializer,
    CategoriaEmpresaSerializer,ResponseCombo,SucursalEditarSerializer,ResponseComboEditar,ResponseProducto,ResponseProductodID,
    ResponsePedidos,ResponsePedidosEditar,CrearPedidoSerializer,EditarPedidoSerializer,ResponseTokenFirebase,PedidosRangoFecha_Sucursal,
    VerCiudad_Serializer,RepartidorDisponible_Serializer,ProductoFinal_Paginator_Serializer,
    # crear combos
    CrearComboSerializer,EditarComboSerializer,VerProductoFinalSerializer,CambiarDisponibleSucursal_Serializer,CrearSucursal_Serializer,
    AgregarHorario_Serializer)
from apps.autenticacion.serializers import UsuarioSerializer,PerfilSerializer
from apps.autenticacion.models import Usuario, Ciudad, Perfil, Horario
from apps.autenticacion.views import get_user_by_token, is_member
from OdinApi_v02.pagination import CustomPagination


# # lista de usuarios
# @api_view(['POST'])
# @permission_classes([IsAuthenticated,permission_required("autenticacion.view_usuario", raise_exception=True),])
# def getUsuariosList(request):
#     us = Usuario.objects.all()
#     data = UsuarioSerializer(us, many=True).data
#     return Response(data)

# @permission_classes([IsAuthenticated,permission_required("autenticacion.view_usuario", raise_exception=True),])
# agregar empresa

def validate_dict_json(data):
    try:
        json.loads(json.dumps(data))
        return True
    except:
        return False



# EMPRESA

# crear empresa
# @renderer_classes((JSONRenderer, BrowsableAPIRenderer))
@swagger_auto_schema(method="POST",request_body=EmpresaSerializer,responses={200:'Se ha agregado la nueva empresa correctamente'},
    operation_id="Crear Empresa")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crearEmpresa(request, format=None):
    empresa = request.data
    obj = EmpresaSerializer(data=empresa)
    # if obj.is_valid():
    #     data = create_obj.data
    #     print(data)
    obj.is_valid(raise_exception=True)
    obj.save()
    return Response({'mensaje':'Se ha agregado la nueva empresa correctamente'})


# modificar empresa
@swagger_auto_schema(method="POST",request_body=EmpresaEditarSerializer,responses={200:'Se ha modificado la empresa correctamente'},
    operation_id="Editar Empresa")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def editar_empresa(request, id_empresa):
    usuario = get_user_by_token(request)
    empresa = revisar_empresa(id_empresa)
    revisar_propietario_empresa(usuario, empresa)
    obj = EmpresaEditarSerializer(empresa, data=request.data, partial=True)
    obj.is_valid(raise_exception=True)
    obj.save()
    return Response({'mensaje':'Se ha modificado la empresa correctamente'})



# obtener todas las empresas
@swagger_auto_schema(method="GET",responses={200:EmpresaSerializer(many=True)},operation_id="Listar Todas Empresa")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_empresas(request):
    empresas = Empresa.objects.all()
    data = EmpresaSerializer(empresas, many=True).data
    return Response(data)



# empresas por usuario
@swagger_auto_schema(method="GET",responses={200:EmpresaSerializer(many=True)},operation_id="Lista de Empresas by Usuario-Token")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getEmpresaByUsuario(request):
    usuario = get_user_by_token(request)
    empresas = Empresa.objects.filter(empresario=usuario)
    if not empresas.exists():
        return Response({'error':'El usuario no tiene ningun empresa asociada'})
    data = EmpresaSerializer(empresas, many=True).data
    return Response(data)



# SUCURSALES

# crear sucursal
@swagger_auto_schema(method="POST",request_body=CrearSucursal_Serializer,responses={200:'Se ha agregado la sucursal correctamente'},
    operation_id="Crear Sucursal")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crearSucursal(request):
    usuario = get_user_by_token(request)
    obj = CrearSucursal_Serializer(data=request.data)
    obj.is_valid(raise_exception=True)
    empresa = revisar_empresa(int(request.data.get('empresa')))
    revisar_propietario_empresa(usuario, empresa)
    obj.save()
    return Response({'mensaje':'Se ha agregado la sucursal correctamente'})



# modificar sucursal
@swagger_auto_schema(method="POST",request_body=SucursalEditarSerializer,responses={200:'Se ha modificado la sucursal correctamente'},
    operation_id="Editar Sucursal")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def editar_sucursal(request,id_sucursal):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    revisar_propietario_sucursal(usuario, sucursal)
    obj = SucursalEditarSerializer(sucursal, data=request.data, partial=True)
    obj.is_valid(raise_exception=True)
    obj.save()
    return Response({'mensaje':'Se ha modificado la sucursal correctamente'})



# lista de sucursales por empresa
@swagger_auto_schema(method="GET",responses={200:SucursalSerializer(many=True)},operation_id="Lista de Sucursales by Empresa",
    operation_description="Para el estado:\n\n\t'A' para activos \n\t'I' para inactivos \n\t'T' para todos las sucursales")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getSucursales(request, id_empresa, estado):
    empresa = revisar_empresa(id_empresa)
    revisar_estado_producto(estado)
    if estado == 'A':
        sucursales = Sucursal.objects.filter(empresa__id=id_empresa, estado=True)
    elif estado == 'I':
        sucursales = Sucursal.objects.filter(empresa__id=id_empresa, estado=False)
    else:
        sucursales = Sucursal.objects.filter(empresa__id=id_empresa)
    
    data = SucursalSerializer(sucursales, many=True).data
    return Response(data)



# lista de todas las sucursales
@swagger_auto_schema(method="GET",responses={200:SucursalSerializer(many=True)},operation_id="Lista de Todas las Sucursales",
    operation_description="Para el estado:\n\n\t'A' para activos \n\t'I' para inactivos \n\t'T' para todos las sucursales")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getAll_Sucursales(request, estado, id_ciudad):
    ciudad = revisar_ciudad(id_ciudad)
    revisar_estado_producto(estado)
    if estado == 'A':
        sucursales = Sucursal.objects.filter(ciudad__id=id_ciudad,estado=True)
    elif estado == 'I':
        sucursales = Sucursal.objects.filter(ciudad__id=id_ciudad,estado=False)
    else:
        sucursales = Sucursal.objects.filter(ciudad__id=id_ciudad)
    
    data = SucursalSerializer(sucursales, many=True).data
    return Response(data)



# obtener sucursal
@swagger_auto_schema(method="GET",responses={200:SucursalSerializer},operation_id="Ver Sucursal")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getSucursal(request, id_sucursal):
    try:
        producto = Sucursal.objects.get(pk=id_sucursal)
    except Exception as e:
        raise NotFound('No se encontro a la sucursal','sucursal_not_found')
    data = SucursalSerializer(producto).data
    return Response(data)


# cambiar disponibilidad de la sucursal
@swagger_auto_schema(method="POST",responses={200:'Se cambio el estado de disponibilidad de la sucursal'},operation_id="Cambiar disponibilidad de la sucursal")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def cambiar_diponible_sucursal(request, id_sucursal):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    revisar_propietario_sucursal(usuario, sucursal)
    obj = CambiarDisponibleSucursal_Serializer(sucursal, data=request.data)
    obj.is_valid(raise_exception=True)
    obj.save()
    try:
        if obj.validated_data['disponible'] is True:
            mensaje = 'La sucursal ahora se encuentra abierta.'
        else:
            mensaje = 'La sucursal ahora se encuentra cerrada'
    except:
        mensaje = 'No se detecto ningun cambio'
    return Response({'mensaje':mensaje})



# lista de ciudades
@swagger_auto_schema(method="GET",responses={200:VerCiudad_Serializer(many=True)},operation_id="Lista Ciudades")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def lista_ciudades(request, estado):
    revisar_estado_AIT(estado)
    if estado == 'A':
        ciudades = Ciudad.objects.filter(estado=True)
    elif estado == 'I':
        ciudades = Ciudad.objects.filter(estado=False)
    else:
        ciudades = Ciudad.objects.all()
    data = VerCiudad_Serializer(ciudades, many=True).data
    return Response(data)



# PRODUCTO


# crear producto
@swagger_auto_schema(method="POST",request_body=ProductoFinalSerializer,responses={200:'Se ha agregado el producto correctamente'},
    operation_id="Crear Producto")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crear_producto(request):
    usuario = get_user_by_token(request)
    obj = ProductoFinalSerializer(data=request.data)
    obj.is_valid(raise_exception=True)
    sucursal = revisar_sucursal(int(request.data['sucursal']))
    revisar_propietario_sucursal(usuario, sucursal)
    obj.save()
    return Response({'mensaje':'Se ha agregado el producto correctamente'})



# editar producto final
@swagger_auto_schema(method="POST",request_body=ProductoFinalEditarSerializer,responses={200:'El producto se modifico correctamente'},
    operation_id="Editar Producto")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def editar_producto(request,id_producto):
    usuario = get_user_by_token(request)
    try:
        producto_final = ProductoFinal.objects.get(pk=id_producto)
    except:
        raise NotFound('No se encontro el producto','not_found_producto')
    if usuario.id != producto_final.sucursal.empresa.empresario.id:
        raise PermissionDenied('El usuario no esta vinculado con el producto','no_permitido')

    obj = ProductoFinalEditarSerializer(producto_final, data=request.data, partial=True)
    obj.is_valid(raise_exception=True)
    obj.save()
    return Response({'mensaje':'El producto se actualizo correctamente'})




# PRODUCTO FINAL - combos + productos normales

# ver producto final
@swagger_auto_schema(method="GET",responses={200:VerProductoFinalSerializer},operation_id="Ver Producto (producto+combo)",
    operation_description="Muestra los detalles de un producto. Si el producto es un combo muestra la lista de estos, caso contrario"
    " muestra false si no lo es.\n\n\tcombo : [ { 'id' : 2, 'nombre' : 'producto2', ..}, { otro producto}]\n\n\tor\n\n\tcombo : false")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_productos_finales(request, id_producto):
    usuario = get_user_by_token(request)
    try:
        producto_final = ProductoFinal.objects.get(pk=id_producto)
    except:
        raise NotFound('No se encontro el producto','producto_not_found')
    data = VerProductoFinalSerializer(producto_final).data
    return Response(data)


# # get productos finales by sucursal
# @swagger_auto_schema(method="GET",responses={200:ProFinalSucursalSerializer},operation_id="Lista de Productos por Sucursal (productos+combos) by Sucursal",
#     operation_description="Devuelve una lista de productos activos o inactivos de una sucursal. En el campo 'combo' si el producto es un combo devuelve true caso contrario false."
#     "\n\n\tcombo : true //es un combo\n\n\tcombo : false //no es combo")
# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# def get_productos_finales_by_sucursal(request, id_sucursal):
#     usuario = get_user_by_token(request)
#     sucursal = revisar_sucursal(id_sucursal)
#     producto_final = ProductoFinal.objects.filter(sucursal__id=id_sucursal)
#     data = ProFinalSucursalSerializer(producto_final, many=True).data
#     return Response(data)

# get productos por estado by sucursal
@swagger_auto_schema(method="GET",responses={200:ProFinalSucursalSerializer},operation_id="Lista de Productos por Sucursal ( productos y combos )",
    operation_description="Devuelve una lista de productos de acuerdo al estado de una sucursal. En el campo 'combo' si el producto es un combo devuelve true caso contrario false."
    "\n\n\tcombo : true //es un combo\n\n\tcombo : false //no es combo\n Para el estado:\n\n\t'A' para activos \n\t'I' para inactivos \n\t'T' para todos los productos")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_productos_estado_by_sucursal(request, id_sucursal, estado):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    estado = revisar_estado_producto(estado)
    
    if estado == 'A':
        producto_final = ProductoFinal.objects.filter(estado=True, sucursal__id=id_sucursal)
    elif estado == 'I':
        producto_final = ProductoFinal.objects.filter(estado=False, sucursal__id=id_sucursal)
    else:
        producto_final = ProductoFinal.objects.filter(sucursal__id=id_sucursal)

    data = ProFinalSucursalSerializer(producto_final, many=True).data
    return Response(data)


# get productos por estado by sucursal - solo productos
@swagger_auto_schema(method="GET",responses={200:ProFinalSucursalSerializer},operation_id="Lista de Productos por Sucursal ( productos )",
    operation_description="Devuelve una lista de solamente productos (no combos) de acuerdo al estado de una sucursal. En el campo 'combo' si el producto es un combo devuelve true caso contrario false."
    "\n\n\tcombo : true //es un combo\n\n\tcombo : false //no es combo\n Para el estado:\n\n\t'A' para activos \n\t'I' para inactivos \n\t'T' para todos los productos")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_productos_estado_productos_by_sucursal(request, id_sucursal, estado):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    estado = revisar_estado_producto(estado)
    
    if estado == 'A':
        producto_final = ProductoFinal.objects.filter(estado=True, sucursal__id=id_sucursal).exclude(id__in=Combo.objects.all().values('combo'))
    elif estado == 'I':
        producto_final = ProductoFinal.objects.filter(estado=False, sucursal__id=id_sucursal).exclude(id__in=Combo.objects.all().values('combo'))
    else:
        producto_final = ProductoFinal.objects.filter(sucursal__id=id_sucursal).exclude(id__in=Combo.objects.all().values('combo'))

    data = ProFinalSucursalSerializer(producto_final, many=True).data
    return Response(data)


# get productos por estado by sucursal - solo combos
@swagger_auto_schema(method="GET",responses={200:ProFinalSucursalSerializer},operation_id="Lista de Productos por Sucursal ( combos )",
    operation_description="Devuelve una lista de productos que sean combos de acuerdo al estado de una sucursal. En el campo 'combo' si el producto es un combo devuelve true caso contrario false."
    "\n\n\tcombo : true //es un combo\n\n\tcombo : false //no es combo\n Para el estado:\n\n\t'A' para activos \n\t'I' para inactivos \n\t'T' para todos los productos")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_productos_estado_combos_by_sucursal(request, id_sucursal, estado):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    estado = revisar_estado_producto(estado)
    
    if estado == 'A':
        producto_final = ProductoFinal.objects.filter(estado=True, sucursal__id=id_sucursal, id__in=Combo.objects.all().values('combo'))
    elif estado == 'I':
        producto_final = ProductoFinal.objects.filter(estado=False, sucursal__id=id_sucursal, id__in=Combo.objects.all().values('combo'))
    else:
        producto_final = ProductoFinal.objects.filter(sucursal__id=id_sucursal, id__in=Combo.objects.all().values('combo'))

    data = ProFinalSucursalSerializer(producto_final, many=True).data
    return Response(data)

# function for list products by combos and normal products

# # obtener productos que no sean combos por sucursal
# @swagger_auto_schema(method="GET", response={200:ProFinalSucursalSerializer}, operation_id="Lista de Productos ")

#   COMBOS


# crear combo
@swagger_auto_schema(method="POST",request_body=CrearComboSerializer,responses={200:'Se ha agregado el combo correctamente'},
    operation_id="Crear Combo", operation_description=("Crea el combo adjuntando los id's y cantidad, en una lista en el campo 'combo' "
    "\n\n\t( [ 'producto_id1-cantidad1', 'producto_id2-cantidad2' ] ).\n\n\tEj. combo:[ '1-2', '2-1' ]"))
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crear_combo(request):
    print(request.data)
    usuario = get_user_by_token(request)
    obj = CrearComboSerializer(data=request.data)
    obj.is_valid(raise_exception=True)

    sucursal = revisar_sucursal(int(request.data['sucursal']))
    revisar_propietario_sucursal(usuario, sucursal)
    productos = obj.validated_data['combo']
    
    combo = obj.save()
    for x in productos:
        line = x.split('-')
        pr = int(line[0])
        ct = int(line[1])
        productos = Combo()
        productos.combo = combo
        productos.producto = ProductoFinal.objects.get(pk=pr)
        productos.cantidad = ct
        productos.save()

    return Response({'mensaje':'Se ha agregado el combo correctamente'})


# editar combo
@swagger_auto_schema(method="POST",request_body=EditarComboSerializer,responses={200:'Se ha modificado el combo correctamente'},
    operation_id="Editar Combo", operation_description=("Modifica el combo adjuntando los id's y cantidad, en una lista en el campo 'combo' "
    "\n\n\t( combo : [ 'producto_id1-cantidad1', 'producto_id2-cantidad2' ] ).\n\n\tEj. combo : [ '1-2', '2-1' ]"))
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def editar_combo(request, id_combo):
    print(request.data)
    usuario = get_user_by_token(request)
    try:
        combo = ProductoFinal.objects.get(pk=id_combo)
    except:
        raise NotFound('No se encontro el combo')
    obj = EditarComboSerializer(combo, data=request.data)
    obj.is_valid(raise_exception=True)

    revisar_propietario_sucursal(usuario, combo.sucursal)
    try:
        productos = obj.validated_data['combo']
        combo = obj.save()
        Combo.objects.filter(combo__id=combo.id).delete()
        for x in productos:
            line = x.split('-')
            pr = int(line[0])
            ct = int(line[1])
            productos = Combo()
            productos.combo = combo
            productos.producto = ProductoFinal.objects.get(pk=pr)
            productos.cantidad = ct
            productos.save()
    except:
        obj.save()

    return Response({'mensaje':'Se ha agregado el combo correctamente'})



# obtener combo - en el urls esta comentado
@swagger_auto_schema(method="GET",responses={200:ProductoFinalSerializer},operation_id="Ver Combo")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getCombo(request, id_combo):
    usuario = get_user_by_token(request)
    try:
        combo = ProductoFinal.objects.get(pk=id_combo)
    except Exception as e:
        return Response({'error':'No existe el combo'})
    try:
        Combo.objects.get(pk=combo.id)
    except:
        return Response({'error':'No existe el combo'})
    # if usuario.id != combo.sucursal.empresa.empresario.id:
    #     return Response({'error':'El usuario no esta asociado con la sucursal'})
    prod_x_combo = ProductoFinal.objects.filter(id__in=ComboProducto.objects.filter(combo=combo.id).values('producto'))
    pr = []
    for p in prod_x_combo:
        pr = pr +[{
            'id':p.id,
            'nombre':p.nombre,
            'precio':str(p.precio),
            'estado':p.estado,
            'sucursal':p.sucursal.id,
            'foto':p.foto.url
        }]
    data = [{
        'id':combo.id,
        'nombre':combo.nombre,
        'descripcion':combo.descripcion,
        'precio':str(combo.precio),
        'estado':combo.estado,
        'foto':combo.foto.url,
        'productos':pr
    }]
    return Response(data)


# obtener combos por sucursal - en el urls esta comentado
@swagger_auto_schema(method="GET",responses={200:ProductoFinalSerializer(many=True)},operation_id="Lista de Combos by Sucursal")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getCombos_by_sucursal(request, id_sucursal):
    usuario = get_user_by_token(request)
    try:
        combos = ProductoFinal.objects.filter(sucursal__id=id_sucursal, id__in=Combo.objects.all().values('producto_final'))
    except Exception as e:
        return Response({'error':'No existe el combo'})
    # if usuario.id != Sucursal.objects.get(pk=id_sucursal).empresa.empresario.id:
    #     return Response({'error':'El usuario no esta asociado con la sucursal'})
    data = []
    for c in combos:
        prod_x_combo = ProductoFinal.objects.filter(sucursal__id=id_sucursal, id__in=ComboProducto.objects.filter(combo=c.id).values('producto'))
        pr = []
        for p in prod_x_combo:
            pr = pr +[{
                'id':p.id,
                'nombre':p.nombre,
                'precio':str(p.precio),
                'estado':p.estado,
                'sucursal':p.sucursal.id,
                'foto':p.foto.url
            }]
        data = data + [{
            'id':c.id,
            'nombre':c.nombre,
            'descripcion':c.descripcion,
            'precio':str(c.precio),
            'estado':c.estado,
            'foto':c.foto.url,
            'productos':pr
        }]
    return Response(data)




# CATEGORIA EMPRESA

# listar categorias
@swagger_auto_schema(method="GET",responses={200:CategoriaEmpresaSerializer},operation_id="Lista de Categorias")
@api_view(['GET'])
@permission_classes((AllowAny,))
def getCategoria(request):
    try:
        categoria = CategoriaEmpresa.objects.filter(estado = True)
    except Exception as e:
        print(e)
        return Response({'error':'No se encontro ninguna categoria'})
    data = CategoriaEmpresaSerializer(categoria, many=True).data
    return Response(data)


# PEDIDOS

# crear pedido deprecado
@swagger_auto_schema(method="POST",request_body=ResponsePedidos,responses={200:'Se ha creado el pedido correctamente'},
    operation_id="Crear Pedido - deprecado")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crear_pedido(request):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    # validar sucursal
    try:
        sucursal = Sucursal.objects.get(pk=int(request.data['sucursal']))
    except:
        return Response({'error':'La sucursal no existe'})
    # validar cliente
    try:
        cliente = Usuario.objects.get(pk=int(request.data['cliente']))
    except:
        return Response({'error':'El cliente no existe'})
    # validar que solo el grupo cliente puedar realizar pedidos
    if not is_member(usuario,'cliente'):
        return Response({'error':'No esta autorizado'})
    # validar productos
    try:
        productos = request.data['productos']
        combos = request.data['combos']
    except:
        return Response({'error':'Hubo un error al cargar los datos de productos o combos'})
    if len(productos) <= 0 and len(combos) <= 0:
        return Response({'error':'Debe ingresar al menos un producto o combo'})
    for p in productos:
        try:
            Producto.objects.get(pk=p['id'])
        except:
            return Response({'error':'El producto id=%s no existe en productos' % (p['id'],)})
    for c in combos:
        try:
            Combo.objects.get(pk=c['id'])
        except:
            return Response({'error':'El combo id=%s no existe en combos' % (c['id'],)})

    pedido = Pedido()
    pedido.cliente = cliente
    pedido.total = Decimal(0.0)
    pedido.estado = 'A'
    pedido.sucursal = sucursal
    pedido.save()
    # sumar los productos y combos
    for p in productos:
        producto_final = ProductoFinal.objects.get(pk=p['id'])
        ppf = PedidoProductoFinal()
        ppf.pedido = pedido
        ppf.producto_final = producto_final
        ppf.save()
        pedido.total = pedido.total + producto_final.precio
        pedido.save()
    
    for c in combos:
        producto_final = ProductoFinal.objects.get(pk=c['id'])
        ppf = PedidoProductoFinal()
        ppf.pedido = pedido
        ppf.producto_final = producto_final
        ppf.save()
        pedido.total = pedido.total + producto_final.precio
        pedido.save()
    
    # try:
    #     producto = request.data
    # except Exception as e:
    #     return Response({'error':'No se pudo realizar la operacion'})
    # obj = PedidoSerializer(data=producto)
    # obj.is_valid(raise_exception=True)
    # obj.save()
    # # pp = PedidoProducto()

    return Response({'mensaje':'Se ha creado el pedido correctamente'})


# crear pedido
@swagger_auto_schema(method="POST",request_body=CrearPedidoSerializer,responses={200:'Se ha creado el pedido correctamente'},
    operation_id="Crear Pedido", operation_description="en productos_final los id's, van tanto de combos como productos normales")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crear_pedido_f(request):
    usuario = get_user_by_token(request)
    # validar que el usuario sea parte del grupo cliente
    if not is_member(usuario,'cliente'):
        raise PermissionDenied('No esta autorizado')
    obj = CrearPedidoSerializer(data=request.data)
    obj.is_valid(raise_exception=True)

    pedido = Pedido()
    pedido.cliente = usuario
    pedido.total = Decimal(0.0)
    pedido.estado = 'A'
    pedido.sucursal = obj.validated_data['sucursal']
    try:
        dir = obj.validated_data['ubicacion']
    except:
        dir = ''
    pedido.ubicacion = dir
    pedido.save()
    for x in obj.validated_data['productos']:
        pf = x['producto_final']
        pedido_producto = PedidoProductoFinal()
        pedido_producto.pedido = pedido
        pedido_producto.producto_final = pf
        pedido_producto.cantidad = x['cantidad']
        pedido_producto.save()
        pedido.total += (pf.precio * x['cantidad'])
        pedido.save()

    return Response({'mensaje':'Se ha creado el pedido correctamente'})



# editar pedido - deprecado
@swagger_auto_schema(method="POST",request_body=ResponsePedidosEditar(many=True),responses={200:'Se ha modificado el pedido correctamente'},
    operation_id="Editar Pedido - Deprecado")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def editar_pedido(request, id_pedido):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
    except:
        return Response({'error':'El pedido no existe'})    
    if pedido.estado == 'F':
        return Response({'error':'El pedido ya no puede ser modificado'})
    # validar que el cliente el cual creo el pedido sea quien pueda realizar cambios
    if usuario.id != pedido.cliente.id:
        return Response({'error':'Usted no realizo el pedido al que desea acceder'})

    # validar productos
    try:
        productos = request.data['productos']
        combos = request.data['combos']
    except:
        return Response({'error':'Hubo un error al cargar los datos de productos o combos'})
    if len(productos) <= 0 and len(combos) <= 0:
        return Response({'error':'Debe ingresar al menos un producto o combo'})
    for p in productos:
        try:
            Producto.objects.get(pk=p['id'])
        except:
            return Response({'error':'El producto id=%s no existe en productos' % (p['id'],)})
    for c in combos:
        try:
            Combo.objects.get(pk=c['id'])
        except:
            return Response({'error':'El combo id=%s no existe en combos' % (c['id'],)})

    pedidosfinal = PedidoProductoFinal.objects.filter(pedido=pedido).delete()
    pedido.total = Decimal(0.0)
    pedido.save()
    # sumar los productos y combos
    for p in productos:
        producto_final = ProductoFinal.objects.get(pk=p['id'])
        ppf = PedidoProductoFinal()
        ppf.pedido = pedido
        ppf.producto_final = producto_final
        ppf.save()
        pedido.total = pedido.total + producto_final.precio
        pedido.save()
    for c in combos:
        producto_final = ProductoFinal.objects.get(pk=c['id'])
        ppf = PedidoProductoFinal()
        ppf.pedido = pedido
        ppf.producto_final = producto_final
        ppf.save()
        pedido.total = pedido.total + producto_final.precio
        pedido.save()

    return Response({'mensaje':'Se ha modificado el pedido correctamente'})


# editar pedidoasd
@swagger_auto_schema(method="POST",request_body=EditarPedidoSerializer,responses={200:'Se ha modificado el pedido correctamente'},
    operation_id="Editar Pedido", operation_description="Modifica los productos de un pedido, por otros. Si desea mantener los productos anteriores, solo adjunte los id's")
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def editar_pedido_f(request,id_pedido):
    usuario = get_user_by_token(request)
    # validar que el usuario sea parte del grupo cliente
    if not is_member(usuario,'cliente'):
        raise PermissionDenied('No esta autorizado')
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
    except:
        raise NotFound('No se encontro el pedido')
    
    obj = EditarPedidoSerializer(pedido,data=request.data)
    obj.is_valid(raise_exception=True)

    try:
        ubicacion = obj.validated_data['ubicacion']
    except:
        ubicacion = pedido.ubicacion
    try:
        obj.validated_data['productos']
        is_productos = True
    except:
        is_productos = False
    
    pedido.ubicacion = ubicacion
    pedido.save()
    if is_productos is True:
        productos = obj.validated_data['productos']
        pedidosfinal = PedidoProductoFinal.objects.filter(pedido=pedido).delete()
        pedido.total = Decimal(0.0)
        for x in obj.validated_data['productos']:
            pf = x['producto_final']
            pedido_producto = PedidoProductoFinal()
            pedido_producto.pedido = pedido
            pedido_producto.producto_final = pf
            pedido_producto.cantidad = x['cantidad']
            pedido_producto.save()
            pedido.total += (pf.precio * x['cantidad'])
            pedido.save()

    return Response({'mensaje':'Se ha modificado el pedido correctamente'})


# obtener token_firebase a partir de la sucursal
@swagger_auto_schema(method="GET", responses={200:ResponseTokenFirebase},operation_id="Obtener Token-Firebase",
    operation_description="Obtiene el token firebase del usuario  a partir del 'id sucursal'")
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_token_firebase(request, id_sucursal):
    data = Sucursal.objects.get(pk=id_sucursal).empresa.empresario.token_firebase
    return Response({'token_firebase':data})



# cambia el estado del pedido a en curso
@swagger_auto_schema(method="POST", responses={200:'El pedido ha sido puesto en curso'},operation_id="Establecer Pedido a en curso",
    operation_description="Cambia el estado del pedido a 'en curso', siempre y cuando este en 'activo'")
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def cambiar_pedido_en_curso(request, id_pedido):
    usuario = get_user_by_token(request)
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
    except:
        raise NotFound('No se encontro el Pedido')
    if pedido.estado == 'F':
        return Response({'detail':'El pedido ya esta finalizado'})
    revisar_propietario_sucursal(usuario,pedido.sucursal)
    pedido.estado = 'E'
    pedido.save()

    return Response({'mensaje':'El pedido ha sido puesto en curso'})


# cambia el estado del pedido a finalizado
@swagger_auto_schema(method="POST", responses={200:'El pedido ha sido finalizado'},operation_id="Establecer Pedido a finalizado",
    operation_description="Cambia el estado del pedido a 'finalizado', siempre y cuando este en 'curso'")
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def cambiar_pedido_en_finalizado(request, id_pedido):
    usuario = get_user_by_token(request)
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
    except:
        raise NotFound('No se encontro el Pedido')
    if pedido.estado == 'A':
        return Response({'detail':'El pedido esta activo'})
    revisar_propietario_sucursal(usuario,pedido.sucursal)
    pedido.estado = 'F'
    pedido.save()

    return Response({'mensaje':'El pedido ha sido finalizado'})


# cambia el estado del pedido a cancelado
@swagger_auto_schema(method="POST", responses={200:'El pedido ha sido cancelado'},operation_id="Establecer Pedido a Cancelado",
    operation_description="Cancela un pedido, no se puede cancelar un pedido que ya se encuentre finalizado")
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def cambiar_pedido_en_cancelado(request, id_pedido):
    usuario = get_user_by_token(request)
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
    except:
        raise NotFound('No se encontro el Pedido')
    if pedido.estado == 'F':
        return Response({'detail':'no se puede cambiar el estado de un pedido finalizado'})
    pedido.estado = 'C'
    pedido.save()

    return Response({'mensaje':'El pedido ha sido cancelado'})

# repartidor

# agregar horario
# @swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Agregar horario a repartidor")


# lista de repartidor por ciudad
@swagger_auto_schema(method="GET",responses={200:PerfilSerializer(many=True)},operation_id="Lista de Repartidores por Ciudad")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def repartidores_by_ciudad(request, id_ciudad):
    # los pedidos se haran por dia laboral
    usuarios = Usuario.objects.filter(groups__name='repartidor',ciudad__id=id_ciudad)
    data = PerfilSerializer(usuarios, many=True).data
    return Response(data)


# cambiar disponibilidad repartidor
@swagger_auto_schema(method="POST",responses={200:'Se ha modificado la disponibilidad'},operation_id="Cambiar Disponibilidad del Repartidor",
    operation_description='Cambia la disponibilidad del repartidor en disponible(L) o no disponible(N).request_body:\n\n\t{\n\t\t"disponible" : "L"\n\t}')
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def cambiar_disponibilidad_repartidor(request):
    usuario = get_user_by_token(request)
    obj = RepartidorDisponible_Serializer(data=request.data)
    obj.is_valid(raise_exception=True)
    mensaje = ''
    if obj.validated_data['disponible'] == 'L':
        Perfil.objects.filter(usuario__id=usuario.id).update(disponibilidad='L')
        mensaje = 'El repartidor ahora esta disponible.'
    else:
        Perfil.objects.filter(usuario__id=usuario.id).update(disponibilidad='N')
        mensaje = 'El repartidor ahora no esta disponible.'
    return Response({'mensaje':mensaje})


# tomar pedido
@swagger_auto_schema(method="POST",responses={200:'asd'},operation_id="Repartidor - Aceptar Pedido",
    operation_description='Permite al repartidor aceptar un pedido.')
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def aceptar_pedido(request,id_pedido):
    usuario = get_user_by_token(request)
    if not is_member(usuario,'repartidor'):
        return Response({'error':'No esta autorizado'})
    pedido = revisar_pedido(id_pedido)
    validar_repartidor_activo(usuario)
    if pedido.estado == 'E':
        if pedido.repartidor is None:
            pedido.repartidor = usuario
            pedido.save()
        else:
            raise PermissionDenied('El pedido ya ha sido tomado por otro usuario')
    else:
        raise PermissionDenied('El pedido no se encuentra en curso')

    return Response({'mensaje':'Ha tomado el pedido'})

# obtener pedidos de todas las sucursales (en curso)
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de todos los Pedidos (DIA)",
    operation_description='Devuelve la lista de todos los pedidos que se encuentren en curso (E) y que  no hallan sido tomados por ningun otro repartidor. ')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_for_repartidor(request):
    usuario = get_user_by_token(request)
    if not is_member(usuario,'repartidor'):
        return Response({'error':'No esta autorizado'})
    # validar que el usuario este disponible y que tenga horarios validos
    validar_repartidor_activo(usuario)
    # los pedidos se haran por dia laboral
    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    print(hora_actual,hora_inicio)
    pedidos = Pedido.objects.filter(sucursal__ciudad__id=usuario.ciudad.id,estado='E',repartidor=None,fecha__gte=hora_inicio,fecha__lte=hora_fin)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)

# obtener pedidos por repartidor del dia
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Pedidos por Repartidor (DIA)",
    operation_description='Devuelve la lista de pedidos del dia por repartidor segun el estado:\n\n\tE = en curso\n\tF = finalizados\n\tC = cancelados')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_repartidor_dia(request,estado):
    usuario = get_user_by_token(request)
    # los pedidos se haran por dia laboral
    estado = revisar_estado_pedido_repartidor(estado)
    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    pedidos = Pedido.objects.filter(estado=estado,repartidor__id=usuario.id,fecha__gte=hora_inicio,fecha__lte=hora_fin)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener pedidos por repartidor semana
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Pedidos por Repartidor (ULTIMOS 7 DIAS)",
    operation_description='Devuelve la lista de pedidos de los ultmos 7 dias por repartidor segun el estado:\n\n\tE = en curso\n\tF = finalizados\n\tC = cancelados')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_repartidor_semana(request,estado):
    usuario = get_user_by_token(request)
    # los pedidos se haran por dia laboral
    estado = revisar_estado_pedido_repartidor(estado)
    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    pedidos = Pedido.objects.filter(estado=estado,repartidor__id=usuario.id,fecha__gte=hora_inicio-timedelta(days=7),fecha__lte=hora_fin)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener pedidos por repartidor rango de fechas
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Pedidos por Repartidor (RANGO DE FECHAS)",
    operation_description='Devuelve la lista de pedidos de los ultmos 7 dias por repartidor segun el estado:\n\n\tE = en curso\n\tF = finalizados\n\tC = cancelados'
        '\nrequest_body:\n\n\t{\n\t\t"fecha_inicio":"YY-MM-DD",\n\t\t"fecha_fin":"YY-MM-DD"\n\t}')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_repartidor_rango(request,estado):
    usuario = get_user_by_token(request)
    fechas = PedidosRangoFecha_Sucursal(data=request.data)
    fechas.is_valid(raise_exception=True)
    # los pedidos se haran por dia laboral
    estado = revisar_estado_pedido_repartidor(estado)
    min_date = make_aware(datetime.combine(fechas.validated_data['fecha_inicio'], time.min))
    max_date = make_aware(datetime.combine(fechas.validated_data['fecha_fin'], time.max))

    pedidos = Pedido.objects.filter(estado=estado,repartidor__id=usuario.id,fecha__gte=min_date,fecha__lte=max_date)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)

# fin repartidor


# obtener pedidos por sucursal
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Pedidos by Sucursal (DIA), estado(A,E,F)")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_sucursal(request, id_sucursal, estado):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    estado = revisar_estado_pedido(estado)
    revisar_propietario_sucursal(usuario, sucursal)
    # los pedidos se haran por dia laboral
    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    pedidos = Pedido.objects.filter(sucursal=sucursal, estado=estado,fecha__gte=hora_inicio,fecha__lte=hora_fin)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener pedidos por sucursal semana
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Pedidos por Sucursal (ULTIMOS 7 DIAS)",
    operation_description='Devuelve la lista de pedidos de los ultmos 7 dias por sucursal segun el estado:\n\n\tA = activo\n\tE = en curso\n\tF = finalizados\n\tC = cancelados')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_sucursal_semana(request,id_sucursal,estado):
    usuario = get_user_by_token(request)
    # los pedidos se haran por dia laboral
    sucursal = revisar_sucursal(id_sucursal)
    estado = revisar_estado_pedido(estado)
    revisar_propietario_sucursal(usuario, sucursal)

    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    pedidos = Pedido.objects.filter(sucursal__id=sucursal.id,estado=estado,fecha__gte=hora_inicio-timedelta(days=7),fecha__lte=hora_fin)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)



# obtener pedidos por sucursal rango de fechas
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Pedidos por Sucursal (RANGO DE FECHAS)",
    operation_description='Devuelve la lista de pedidos en el rango de fechas segun el estado:\n\n\tA = activo\n\tE = en curso\n\tF = finalizados\n\tC = cancelados'
        '\nrequest_body:\n\n\t{\n\t\t"fecha_inicio":"YY-MM-DD",\n\t\t"fecha_fin":"YY-MM-DD"\n\t}')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_sucursal_rango(request,id_sucursal, estado):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    estado = revisar_estado_pedido(estado)
    revisar_propietario_sucursal(usuario, sucursal)

    fechas = PedidosRangoFecha_Sucursal(data=request.data)
    fechas.is_valid(raise_exception=True)
    # los pedidos se haran por dia laboral
    min_date = make_aware(datetime.combine(fechas.validated_data['fecha_inicio'], time.min))
    max_date = make_aware(datetime.combine(fechas.validated_data['fecha_fin'], time.max))

    pedidos = Pedido.objects.filter(sucursal__id=sucursal.id, estado=estado,fecha__gte=min_date,fecha__lte=max_date)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener pedidos activos por empresa
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Pedidos by Empresa, estado(A,E,F)")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_empresa(request, id_empresa, estado):
    usuario = get_user_by_token(request)
    empresa = revisar_empresa(id_empresa)
    estado = revisar_estado_pedido(estado)
    revisar_propietario_empresa(usuario, empresa)
    # los pedidos se haran por dia laboral
    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    
    pedidos = Pedido.objects.filter(sucursal__empresa=empresa, estado=estado,fecha__gte=hora_inicio,fecha__lte=hora_fin)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener todos los pedidos por sucursal
@swagger_auto_schema(method="GET",responses={200:PedidosSucursalCustomSerializer(many=True)},operation_id="Lista de Todos Pedidos by Sucursal, estado(A,E,F)")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_todos_pedidos_by_sucursal(request, id_sucursal, estado):
    usuario = get_user_by_token(request)
    sucursal = revisar_sucursal(id_sucursal)
    estado = revisar_estado_pedido(estado)
    revisar_propietario_sucursal(usuario, sucursal)

    pedidos = Pedido.objects.filter(sucursal=sucursal, estado=estado)
    data = PedidosSucursalCustomSerializer(pedidos, many=True).data
    return Response(data)


# def revisar_usuario(request):
#     try:
#         return get_user_by_token(request)
#     except:
#         return Response({'error':'No se encontro al usuario'},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getp(request):
    pedidos = Pedido.objects.filter(cliente__id=2)
    data = PedidosCustomSerializer(pedidos, many=True).data
    return Response(data)

# cambia el estado del pedido a finalizado
@swagger_auto_schema(method="POST", responses={200:'El pedido ha sido finalizado'},operation_id="Establecer Pedido a finalizado - cliente",
    operation_description="Cambia el estado del pedido a 'finalizado', siempre y cuando este en 'curso'")
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def cambiar_pedido_en_finalizado_cliente(request, id_pedido):
    usuario = get_user_by_token(request)
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
    except:
        raise NotFound('No se encontro el Pedido')
    if pedido.estado != 'E':
        return Response({'detail':'El pedido no esta en curso'})
    if pedido.cliente.id != usuario.id:
        raise PermissionDenied('Usted no realizo el pedido')
    pedido.estado = 'F'
    pedido.save()

    return Response({'mensaje':'El pedido ha sido finalizado'})

# a los pedidos para el cliente no lo envio el objeto completo de cliente(solo su id).. solo a las empresa se les envia completo el cliente
# obtener pedidos por cliente dia
@swagger_auto_schema(method="GET",responses={200:PedidosCustomSerializer(many=True)},operation_id="Lista de Pedidos por Cliente (DIA)",
    operation_description='Devuelve la lista de pedidos del dia por cliente segun el estado:\n\n\tA = activo\n\tE = en curso\n\tF = finalizados\n\tC = cancelados')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_estado_cliente(request, estado):
    usuario = get_user_by_token(request)
    if not is_member(usuario,'cliente'):
        return Response({'error':'No esta autorizado'})
    estado = revisar_estado_pedido(estado)

    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    pedidos = Pedido.objects.filter(cliente__id=usuario.id,estado=estado,fecha__gte=hora_inicio,fecha__lte=hora_fin)
    data = PedidosCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener pedidos por cliente semana
@swagger_auto_schema(method="GET",responses={200:PedidosCustomSerializer(many=True)},operation_id="Lista de Pedidos por Cliente (ULTIMOS 7 DIAS)",
    operation_description='Devuelve la lista de pedidos de la semana por cliente segun el estado:\n\n\tA = activo\n\tE = en curso\n\tF = finalizados\n\tC = cancelados')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_estado_cliente_semana(request, estado):
    usuario = get_user_by_token(request)
    if not is_member(usuario,'cliente'):
        return Response({'error':'No esta autorizado'})
    estado = revisar_estado_pedido(estado)

    hora_actual = make_aware(datetime.now())
    hora_inicio = get_hora_apertura(hora_actual)
    hora_fin = hora_actual
    pedidos = Pedido.objects.filter(cliente__id=usuario.id,estado=estado,fecha__gte=hora_inicio-timedelta(days=7),fecha__lte=hora_fin)
    data = PedidosCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener pedidos por cliente rango
@swagger_auto_schema(method="GET",responses={200:PedidosCustomSerializer(many=True)},operation_id="Lista de Pedidos por Cliente (RANGO DE FECHAS)",
    operation_description='Devuelve la lista de pedidos de acuerdo al rango de fechas por cliente segun el estado:\n\n\tA = activo\n\tE = en curso\n\tF = finalizados\n\tC = cancelados'
        '\nrequest_body:\n\n\t{\n\t\t"fecha_inicio":"YY-MM-DD",\n\t\t"fecha_fin":"YY-MM-DD"\n\t}')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_estado_cliente_rango(request, estado):
    usuario = get_user_by_token(request)
    if not is_member(usuario,'cliente'):
        return Response({'error':'No esta autorizado'})
    estado = revisar_estado_pedido(estado)
    fechas = PedidosRangoFecha_Sucursal(data=request.data)
    fechas.is_valid(raise_exception=True)

    min_date = make_aware(datetime.combine(fechas.validated_data['fecha_inicio'], time.min))
    max_date = make_aware(datetime.combine(fechas.validated_data['fecha_fin'], time.max))
    pedidos = Pedido.objects.filter(cliente__id=usuario.id,estado=estado,fecha__gte=min_date,fecha__lte=max_date)
    data = PedidosCustomSerializer(pedidos, many=True).data
    return Response(data)



# a los pedidos para el cliente no lo envio el objeto completo de cliente(solo su id).. solo a las empresa se les envia completo el cliente
# obtener pedidos activos por cliente comentado
# @swagger_auto_schema(method="GET",responses={200:PedidosCustomSerializer(many=True)},operation_id="Lista de Pedidos Activo y en Cursp by Cliente-Token")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_activos_by_cliente(request):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    if not is_member(usuario,'cliente'):
        return Response({'error':'No esta autorizado'})
    pedidos = Pedido.objects.filter(Q(cliente__id=usuario.id) & ( Q(estado='A') | Q(estado='E')) )
    data = PedidosCustomSerializer(pedidos, many=True).data
    return Response(data)


# obtener pedidos finalizados por cliente comentado
# @swagger_auto_schema(method="GET",responses={200:PedidosCustomSerializer(many=True)},operation_id="Lista de Pedidos Finalizados by Cliente-Token")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_pedidos_finalizados_by_cliente(request):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    if not is_member(usuario,'cliente'):
        return Response({'error':'No esta autorizado'})
    pedidos = Pedido.objects.filter(cliente__id=usuario.id, estado='F')
    data = PedidosCustomSerializer(pedidos, many=True).data
    return Response(data)


def cargar_pedidos(pedidos):
    data = []
    for p in pedidos:
        productos = []
        combos = []
        pf = PedidoProductoFinal.objects.filter(pedido=p['id']).values('id','pedido','producto_final')
        for x in pf:
            try:
                Producto.objects.get(pk=x['producto_final'])
                prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
                productos = productos + [{
                    'id':prod_f.id,
                    'nombre':prod_f.nombre,
                    'descripcion':prod_f.descripcion,
                    'precio':str(prod_f.precio),
                    'estado':prod_f.estado,
                    'foto':prod_f.foto.url,
                    'sucursal':prod_f.id
                }]
            except Exception as e:
                try:
                    Combo.objects.get(pk=x['producto_final'])
                    prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
                    prod = ComboProducto.objects.filter(combo=x['producto_final']).values('id','combo','producto')
                    pro2 = []
                    for b in prod:
                        p2 = ProductoFinal.objects.get(pk=b['producto'])
                        pro2 = pro2 + [{
                            'id':p2.id,
                            'nombre':p2.nombre,
                            'descripcion':p2.descripcion,
                            'precio':str(p2.precio),
                            'estado':p2.estado,
                            'foto':p2.foto.url,
                            'sucursal':p2.id
                        }]
                    combos = combos + [{
                        'id':prod_f.id,
                        'nombre':prod_f.nombre,
                        'descripcion':prod_f.descripcion,
                        'precio':str(prod_f.precio),
                        'estado':prod_f.estado,
                        'foto':prod_f.foto.url,
                        'sucursal':prod_f.id,
                        'productos':pro2
                    }]
                    

                except Exception as e:
                    return Response({'error':'Hubo un error al cargar los datos'})
        data = data + [{
            'cliente':p['cliente'],
            'total':str(p['total']),
            'fecha':p['fecha'],
            'estado':p['estado'],
            'sucursal':p['sucursal'],
            'productos':productos,
            'combos':combos
        }]
    return data


# pedidos por sucursal inactivos
@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_sucursal_inactivos(request, id_sucursal):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    try:
        sucursal = Sucursal.objects.get(pk=id_sucursal)
    except:
        return Response({'error':'La Sucursal no existe'})
    # validar que el usuario sea propietario de la sucursal
    if usuario.id != sucursal.empresa.empresario.id:
        return Response({'error':'El usuario no esta asociado a la sucursal'})

    pedidos = Pedido.objects.filter(sucursal=sucursal,estado='I').values('id','fecha','cliente','estado','total','sucursal')
    data = []
    for p in pedidos:
        productos = []
        combos = []
        pf = PedidoProductoFinal.objects.filter(pedido=p['id']).values('id','pedido','producto_final')
        for x in pf:
            try:
                Producto.objects.get(pk=x['producto_final'])
                prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
                productos = productos + [{
                    'id':prod_f.id,
                    'nombre':prod_f.nombre,
                    'descripcion':prod_f.descripcion,
                    'precio':str(prod_f.precio),
                    'estado':prod_f.estado,
                    'foto':prod_f.foto.url,
                    'sucursal':prod_f.id
                }]
            except Exception as e:
                try:
                    Combo.objects.get(pk=x['producto_final'])
                    prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
                    prod = ComboProducto.objects.filter(combo=x['producto_final']).values('id','combo','producto')
                    pro2 = []
                    for b in prod:
                        p2 = ProductoFinal.objects.get(pk=b['producto'])
                        pro2 = pro2 + [{
                            'id':p2.id,
                            'nombre':p2.nombre,
                            'descripcion':p2.descripcion,
                            'precio':str(p2.precio),
                            'estado':p2.estado,
                            'foto':p2.foto.url,
                            'sucursal':p2.id
                        }]
                    combos = combos + [{
                        'id':prod_f.id,
                        'nombre':prod_f.nombre,
                        'descripcion':prod_f.descripcion,
                        'precio':str(prod_f.precio),
                        'estado':prod_f.estado,
                        'foto':prod_f.foto.url,
                        'sucursal':prod_f.id,
                        'productos':pro2
                    }]
                    

                except Exception as e:
                    return Response({'error':'Hubo un error al cargar los datos'})
        data = data + [{
            'cliente':p['cliente'],
            'total':str(p['total']),
            'fecha':p['fecha'],
            'estado':p['estado'],
            'sucursal':p['sucursal'],
            'productos':productos,
            'combos':combos
        }]
        
    return Response(data)




# pedidos por sucursal espera
@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def get_pedidos_by_sucursal_espera(request, id_sucursal):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    try:
        sucursal = Sucursal.objects.get(pk=id_sucursal)
    except:
        return Response({'error':'La Sucursal no existe'})
    # validar que el usuario sea propietario de la sucursal
    if usuario.id != sucursal.empresa.empresario.id:
        return Response({'error':'El usuario no esta asociado a la sucursal'})

    pedidos = Pedido.objects.filter(sucursal=sucursal,estado='E').values('id','fecha','cliente','estado','total','sucursal')
    data = []
    for p in pedidos:
        productos = []
        combos = []
        pf = PedidoProductoFinal.objects.filter(pedido=p['id']).values('id','pedido','producto_final')
        for x in pf:
            try:
                Producto.objects.get(pk=x['producto_final'])
                prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
                productos = productos + [{
                    'id':prod_f.id,
                    'nombre':prod_f.nombre,
                    'descripcion':prod_f.descripcion,
                    'precio':str(prod_f.precio),
                    'estado':prod_f.estado,
                    'foto':prod_f.foto.url,
                    'sucursal':prod_f.id
                }]
            except Exception as e:
                try:
                    Combo.objects.get(pk=x['producto_final'])
                    prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
                    prod = ComboProducto.objects.filter(combo=x['producto_final']).values('id','combo','producto')
                    pro2 = []
                    for b in prod:
                        p2 = ProductoFinal.objects.get(pk=b['producto'])
                        pro2 = pro2 + [{
                            'id':p2.id,
                            'nombre':p2.nombre,
                            'descripcion':p2.descripcion,
                            'precio':str(p2.precio),
                            'estado':p2.estado,
                            'foto':p2.foto.url,
                            'sucursal':p2.id
                        }]
                    combos = combos + [{
                        'id':prod_f.id,
                        'nombre':prod_f.nombre,
                        'descripcion':prod_f.descripcion,
                        'precio':str(prod_f.precio),
                        'estado':prod_f.estado,
                        'foto':prod_f.foto.url,
                        'sucursal':prod_f.id,
                        'productos':pro2
                    }]
                    

                except Exception as e:
                    return Response({'error':'Hubo un error al cargar los datos'})
        data = data + [{
            'cliente':p['cliente'],
            'total':str(p['total']),
            'fecha':p['fecha'],
            'estado':p['estado'],
            'sucursal':p['sucursal'],
            'productos':productos,
            'combos':combos
        }]
        
    return Response(data)



# ver pedido
@swagger_auto_schema(method="GET",responses={200:PedidosCustomSerializer},operation_id="Ver Pedido")
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ver_pedido(request, id_pedido):
    try:
        usuario = get_user_by_token(request)
    except:
        return Response({'error':'No se encontro al usuario'})
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
    except:
        return Response({'error':'El pedido no existe'})
    # validar que el usuario sea propietario de la sucursal
    if usuario.id != pedido.sucursal.empresa.empresario.id:
        return Response({'error':'El usuario no esta asociado a la sucursal'})

    data = []
    productos = []
    combos = []
    pf = PedidoProductoFinal.objects.filter(pedido=pedido.id).values('id','pedido','producto_final')
    for x in pf:
        try:
            Producto.objects.get(pk=x['producto_final'])
            prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
            productos = productos + [{
                'id':prod_f.id,
                'nombre':prod_f.nombre,
                'descripcion':prod_f.descripcion,
                'precio':str(prod_f.precio),
                'estado':prod_f.estado,
                'foto':prod_f.foto.url,
                'sucursal':prod_f.id
            }]
        except Exception as e:
            try:
                Combo.objects.get(pk=x['producto_final'])
                prod_f = ProductoFinal.objects.get(pk=x['producto_final'])
                prod = ComboProducto.objects.filter(combo=x['producto_final']).values('id','combo','producto')
                pro2 = []
                for b in prod:
                    p2 = ProductoFinal.objects.get(pk=b['producto'])
                    pro2 = pro2 + [{
                        'id':p2.id,
                        'nombre':p2.nombre,
                        'descripcion':p2.descripcion,
                        'precio':str(p2.precio),
                        'estado':p2.estado,
                        'foto':p2.foto.url,
                        'sucursal':p2.id
                    }]
                combos = combos + [{
                    'id':prod_f.id,
                    'nombre':prod_f.nombre,
                    'descripcion':prod_f.descripcion,
                    'precio':str(prod_f.precio),
                    'estado':prod_f.estado,
                    'foto':prod_f.foto.url,
                    'sucursal':prod_f.id,
                    'productos':pro2
                }]
                

            except Exception as e:
                return Response({'error':'Hubo un error al cargar los datos'})
    data = data + [{
        'id':pedido.id,
        'cliente':pedido.cliente.id,
        'total':str(pedido.total),
        'fecha':pedido.fecha,
        'estado':pedido.estado,
        'sucursal':pedido.sucursal.id,
        'productos':productos,
        'combos':combos
    }]
        
    return Response(data)


# test
# def serialize_producto(pr:ProductoFinal) -> Dict[str, Any]:
#     # print('INICIO')
#     # if pr.foto:
#     #     print('SUPSER RATAS')
#     return {
#         'id': pr.id,
#         'nombre':pr.nombre,
#         'descripcion':pr.descripcion,
#         'precio':pr.precio,
#         'estado':pr.estado,
#         'sucursal':str(pr.sucursal),
#         'foto':pr.foto.url if pr.foto else None
#     }

@api_view(['GET'])
@permission_classes([AllowAny,])
def lista_productos_paginator(request):
    
    paginator = CustomPagination()
    # testcode = '''
    # ProductoFinal.objects.all()
    # '''
    # print(timeit.timeit(stmt=testcode))
    t0 = ti.time()
    query_set = ProductoFinal.objects.all()
    context = paginator.paginate_queryset(query_set, request)
    serializer = ProductoFinal_Paginator_Serializer(context, many=True)
    data = paginator.get_paginated_response(serializer.data)
    t1 = ti.time()
    print('TIEMPO DEL SEGMENTE: ',"{:.6f}".format(t1-t0))
    return data

@api_view(['GET'])
@permission_classes([AllowAny,])
def lista_productos_paginator2(request):
    paginator = CustomPagination()
    t0 = ti.time()
    query_set = ProductoFinal.objects.filter(id__gte=1,id__lte=5000)
    # context = paginator.paginate_queryset(query_set, request)
    data = ProFinalSucursalSerializer(query_set, many=True).data
    # data = paginator.get_paginated_response(serializer.data)
    t1 = ti.time()
    print('TIEMPO DEL SEGMENTE: ',"{:.6f}".format(t1-t0))
    return Response(data)


# class MyListAPIView(generics.ListAPIView):
#     permission_classes = [AllowAny,]
#     queryset = ProductoFinal.objects.all()
#     serializer_class = ProFinalSucursalSerializer
#     pagination_class = CustomPagination



def get_hora_apertura(fecha):
    hora_apertura = fecha.replace(hour=6, minute=00, second=00)
    hora_inicio = 1
    if fecha >= hora_apertura:
        hora_inicio = hora_apertura
    elif fecha < hora_apertura:
        hora_inicio = hora_apertura-timedelta(days=1)
    return hora_inicio

def revisar_empresa(id_empresa):
    try:
        empresa = Empresa.objects.get(pk=id_empresa)
        return empresa
    except:
        raise NotFound('No se encontro a la empresa','empresa not found')

def revisar_sucursal(id_sucursal):
    try:
        sucursal = Sucursal.objects.get(pk=id_sucursal)
        return sucursal
    except:
        raise NotFound('No se encontro la sucursal','sucursal_not_found')

def revisar_pedido(id_pedido):
    try:
        pedido = Pedido.objects.get(pk=id_pedido)
        return pedido
    except:
        raise NotFound('No se encontro el pedido')

def revisar_estado_pedido(estado):
    if not(estado == 'A' or estado == 'E' or estado == 'F' or estado == 'C'):
        raise NotFound('No existe la ruta','empresa not found')
    return estado

def revisar_estado_pedido_repartidor(estado):
    if not(estado == 'E' or estado == 'F' or estado == 'C'):
        raise NotFound('No existe la ruta')
    return estado

def revisar_estado_producto(estado):
    if not(estado == 'A' or estado == 'I' or estado == 'T'):
        raise NotFound('No existe la ruta','empresa not found')
    return estado

def revisar_estado_AIT(estado):
    if not (estado == 'A' or estado == 'I' or estado == 'T'):
        raise NotFound('No se encontro la ruta')
    return estado

def revisar_propietario_sucursal(usuario, sucursal):
    if usuario.id != sucursal.empresa.empresario.id:
        raise PermissionDenied('El usuario no esta asociado a la sucursal','no_permitido')
    return True

def revisar_propietario_empresa(usuario, empresa):
    if usuario.id != empresa.empresario.id:
        raise PermissionDenied('El usuario no esta asociado a la empresa','no_permitido')
    return True

def revisar_sucursales_by_empresa(empresa):
    try:
        sucursales = Sucursal.objects.filter(empresa=empresa)
        return sucursales
    except:
        raise NotFound('No se encontro a la sucursal','sucursales_not_found')
    
def revisar_ciudad(id_ciudad):
    try:
        ciudad = Ciudad.objects.get(pk=id_ciudad)
        return ciudad
    except:
        raise NotFound('No se encontro la ciudad')

def validar_repartidor_activo(usuario):
    if usuario.is_active is False:
        raise PermissionDenied('El usuario se encuentra de baja en el sistema')
    try:
        perfil = Perfil.objects.get(usuario__id=usuario.id)
    except:
        raise PermissionDenied('El usuario no tiene el perfil activo')
    if perfil.disponibilidad != 'L':
        raise PermissionDenied('El usuario no esta disponible')
    ini = datetime.now().time()
    if Horario.objects.filter(usuario__id=usuario.id,entrada__lte=ini,salida__gte=ini,estado=True).exists() is False:
        raise PermissionDenied('El usuario no esta en horario de trabajo')
    return True

# class AddImage (generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#     #queryset = Img.objects.all()
#     serializer_class = ProdcutoSerializer
#     def perform_create(self, serializer):
#         serializer.save()
