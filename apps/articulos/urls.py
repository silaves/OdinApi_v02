from django.urls import path
from . import views

urlpatterns = [
    # TIENDAS
    path('tienda/crear/', views.crear_tienda, name='Crear Tienda'),
    path('tienda/<int:id_tienda>/editar/', views.editar_tienda, name='Editar Tienda'),
    path('tienda/<int:id_tienda>/ver/', views.ver_tienda, name='Ver Tienda'),
    path('tienda/<int:id_tienda>/foto/agregar/', views.agregar_foto_tienda, name='Agregar Imagen a Tienda'),
    path('tienda/foto/<int:id_foto>/eliminar/', views.eliminar_foto_tienda, name='Eliminar Imagen a Tienda'),
    path('tienda/<str:estado>/lista/', views.listar_tiendas_por_estado, name='Lista Tiendas por estado'),
    # CATEGORIAS ARTICULOS
    # path('categoria/crear/', views.crear_categoria, name='Crear Categoria Articulos'),
    path('categoria/<str:estado>/lista/', views.lista_categoria_estado, name='Listar Categorias'),
    path('categoria/<int:id_categoria>/lista/hijos/', views.lista_subcategorias_hijo, name='Listar Categoria Hijos'),

    # ARTICULOS
    # path('articulo/crear/', views.crear_articulo, name='Crear Articulo'),
]