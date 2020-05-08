import os
from django.conf import settings
from django.shortcuts import render
from django.db.models import F

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

from drf_yasg.utils import swagger_auto_schema

from apps.empresa.models import CategoriaEmpresa
from apps.autenticacion.views import get_user_by_token
from .models import *
from .serializers import *

# TIENDA

# crear tienda
@swagger_auto_schema(method='POST', request_body=CrearTienda_Serializer, responses={200:'Se ha creado la tienda correctamente'},
    operation_id='Crear Tienda', operation_description='Crea una nueva tienda')
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def crear_tienda(request):
    usuario = get_user_by_token(request)
    obj = CrearTienda_Serializer(data=request.data)
    obj.is_valid(raise_exception=True)

    empresa = Empresa()
    empresa.nombre = obj.validated_data['nombre']
    empresa.descripcion = obj.validated_data['descripcion']
    empresa.empresario = usuario
    try:
        empresa.categoria = CategoriaEmpresa.objects.get(nombre='articulos')
    except:
        raise NotFound('No se encontro la categoria articulos.')
    empresa.save()
    tienda = Tienda()
    tienda.telefono = obj.validated_data['telefono']
    tienda.direccion = obj.validated_data['direccion']
    try:
        tienda.hora_inicio = obj.validated_data['hora_inicio']
        tienda.hora_fin = obj.validated_data['hora_fin']
    except:
        pass
    tienda.empresa = empresa
    tienda.save()
    return Response({'mensaje':'Se ha creado la tienda correctamente'})


# editar tienda
@swagger_auto_schema(method='POST', request_body=CrearTienda_Serializer, responses={200:'Se ha modificado la tienda correctamente'},
    operation_id='Editar Tienda', operation_description='Modifica uno o mas campos de la tienda.')
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def editar_tienda(request, id_tienda):
    usuario = get_user_by_token(request)
    tienda = get_tienda(id_tienda)
    obj = CrearTienda_Serializer(tienda, data=request.data, partial=True)
    obj.is_valid(raise_exception=True)
    
    tienda_s = EditarTienda_Serializer(tienda, data=request.data, partial=True)
    tienda_s.is_valid(raise_exception=True)
    tienda_s.save()
    empresa_s = EditarEmpresa_Serializer(tienda.empresa, data=request.data, partial=True)
    empresa_s.is_valid(raise_exception=True)
    empresa_s.save()
    
    return Response({'mensaje':'Se ha modificado la tienda correctamente'})


# ver tienda
@swagger_auto_schema(method='GET', responses={200:CrearTienda_Serializer}, operation_id='Ver Tienda',
    operation_description='Obtiene los campos de la tienda de acuerdo al id_tienda')
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def ver_tienda(request, id_tienda):
    tienda = get_tienda(id_tienda)
    data = VerTienda_Serializer(tienda).data
    return Response(data)


# Listar Tiendas por estado
@swagger_auto_schema(method='GET', responses={200:VerTienda_Serializer(many=True)}, operation_id='Lista de Tiendas por estado',
    operation_description='Devuelve la lista de tiendas de acuerdo al estado:\n\n\tA = Activo\n\tI = Inactivo\n\tT = Todos (activos e inactivos)')
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def listar_tiendas_por_estado(request, estado):
    estado = revisar_estado_tienda(estado)
    if estado == 'A':
        tiendas = Tienda.objects.filter(empresa__estado=True)
    elif estado == 'I':
        tiendas = Tienda.objects.filter(empresa__estado=False)
    else:
        tiendas = Tienda.objects.filter()
    data = VerTienda_Serializer(tiendas, many=True,context={'request': request}).data
    return Response(data)


# agregar foto a tienda
@swagger_auto_schema(method='POST', request_body=AgregarFotoTienda_Serializer,responses={200:'Se ha agregado la imagen'}, 
    operation_id='Agregar foto a tienda',operation_description='Agrega una foto a una tienda')
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def agregar_foto_tienda(request, id_tienda):
    usuario = get_user_by_token(request)
    revisar_tienda(id_tienda)
    revisar_propietario_tienda(usuario, id_tienda)
    obj = AgregarFotoTienda_Serializer(data=request.data)
    obj.is_valid(raise_exception=True)
    obj.save()
    return Response({'mensaje':'Se ha agregado la imagen'})


# eliminar foto de tienda
@swagger_auto_schema(method='POST', responses={200:'Se ha eliminado la imagen'}, operation_id='Eliminar foto de tienda',
    operation_description='Elimina una foto de una tienda')
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def eliminar_foto_tienda(request, id_foto):
    usuario = get_user_by_token(request)
    foto_f = revisar_foto_tienda(id_foto)
    revisar_propietario_foto_tienda(usuario, id_foto)
    path = foto_f.foto.url
    foto_f.delete()
    eliminar_archivo(path)
    return Response({'mensaje':'Se ha eliminado la imagen'})


# CATEGORIAS ARTICULO

# @api_view(['POST'])
# @permission_classes([IsAuthenticated,])
def crear_categoria(request):
    # obj = CrearCategoria_Serializer(data=request.data)
    # obj.is_valid(raise_exception=True)
    # return Response({'mensaje':'Se ha agregado la categoria'})
    return 1

def editar_categoria(request, id_categoria):
    return 1

def agregar_sub_categoria(request):
    return 1

def dar_baja_categoria(request, id_categoria):
    return 1

def dar_alta_categeoria(request, id_categoria):
    return 1

def ver_categoria(request, id_categoria):
    return 1


# listar categorias por estado
@swagger_auto_schema(method='GET', responses={200:VerCategoriaHijosArticulo_Serializer}, operation_id='Lista de Categorias por Estado ( arbol )',
    operation_description='Devuelve las categorias y subcategorias segun el estado:\n\n\tA = activos\n\tT = todos')
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def lista_categoria_estado(request, estado):
    revisar_estado_categoria(estado)
    cate = SubCategoriaArticulo.objects.all().values('hijo')
    if estado == 'A':
        categorias = CategoriaArticulo.objects.filter(estado=True).exclude(id__in=cate)
    else:
        categorias = CategoriaArticulo.objects.all().exclude(id__in=cate)

    data = VerCategoriaHijosArticulo_Serializer(categorias, many=True, context={'_estado':estado}).data
    return Response(data)


# devuelve la lista de subcategorias de el id_categoria, sus hijos
@swagger_auto_schema(method='GET', responses={200:VerSubCategoriaArticulo_Serializer}, operation_id='Ver sub categorias de un categoria',
    operation_description='Devuelve la categoria y sus sub categorias de la misma')
@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def lista_subcategorias_hijo(request, id_categoria):
    categoria = CategoriaArticulo.objects.get(pk=id_categoria)
    # categoria = SubCategoriaArticulo.objects.filter()
    # data = VerCategoriaHijosArticulo_Serializer(categoria).data
    data = VerCategoriaHijosArticulo_Serializer(categoria, context={'_estado':'T'}).data
    return Response(data)

# ARTICULOS

# crear articulo
@swagger_auto_schema(method='POST', responses={200:CrearArticulo_Serializer}, operation_id='Crear articulo',
    operation_description='asd')
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def crear_articulo(request):
    usuario = get_user_by_token(request)
    obj = CrearArticulo_Serializer(data=request.data, context={'id_usuario':usuario.id})
    obj.is_valid(raise_exception=True)
    return Response({'mensaje':'Se ha creado el articulo'})

# funciones auxiliares

def eliminar_archivo(path):
    full_path = settings.BASE_DIR+path
    if os.path.isfile(full_path):
        os.remove(full_path)
def revisar_estado_categoria(estado):
    if not(estado == 'A' or estado == 'T'):
        raise NotFound('No existe la ruta')
    return estado

def revisar_tienda(id_tienda):
    try:
        tienda = Tienda.objects.get(pk=id_tienda)
    except:
        raise NotFound('No se encontro la tienda')
    return tienda

def revisar_foto_tienda(id_foto):
    try:
        foto = FotoTienda.objects.get(pk=id_foto)
    except:
        raise NotFound('No se encontro la imagen')
    return foto

def revisar_propietario_foto_tienda(usuario, id_foto):
    if not FotoTienda.objects.filter(pk=id_foto, tienda__empresa__empresario__id=usuario.id).exists():
        raise PermissionDenied('Usted no es propietario de la tienda')
    return True

def revisar_propietario_tienda(usuario, id_tienda):
    if not Tienda.objects.filter(id=id_tienda,empresa__empresario__id=usuario.id).exists():
        raise PermissionDenied('Usted no es propietario de la tienda')
    return True

def revisar_estado_tienda(estado):
    if not(estado == 'A' or estado == 'I' or estado == 'T'):
        raise NotFound('No existe la ruta')
    return estado

def get_tienda(id_tienda):
    try:
        tienda = Tienda.objects.get(pk=id_tienda)
        return tienda
    except:
        raise NotFound('No se encontro la tienda')