from django.urls import path
from . import views

urlpatterns = [
    # EMPRESA
    path('empresa/crear/', views.crearEmpresa, name='Crear Empresa'),
    path('empresa/<int:id_empresa>/editar/', views.editar_empresa, name='Modificar Empresa'),
    path('empresa/usuario/', views.getEmpresaByUsuario, name='Lista Empresas por Usuario'),
    path('empresa/lista/', views.get_empresas, name='Lista todas las Empresas'),
    # SUCURSAL
    path('empresa/sucursal/crear/', views.crearSucursal, name='Crear Sucursal'),
    path('empresa/sucursal/<int:id_sucursal>/editar/', views.editar_sucursal, name='Modificar Sucursal'),
    path('empresa/sucursal/lista/', views.getAll_Sucursales, name='Lista todas Sucursales'),
    path('empresa/<int:id_empresa>/sucursal/lista/', views.getSucursales, name='Lista de Sucursales por Empresa'),
    path('empresa/<int:id_empresa>/sucursal/<int:id_sucursal>/', views.getSucursal, name='Obtener Sucursal'),
    path('empresa/sucursal/<int:id_sucursal>/disponible/', views.cambiar_diponible_sucursal, name='Cambiar Disponibilidad Sucursal'),

    path('empresa/sucursal/<int:id_sucursal>/token_firebase/',views.get_token_firebase, name='Obtener Toke Firebase'),
    # PRODUCTO
    path('empresa/sucursal/producto/crear/', views.crear_producto, name='Crear Producto'),
    path('empresa/sucursal/producto/<int:id_producto>/editar/', views.editar_producto, name='Editar Producto'),
    path('empresa/sucursal/producto/<int:id_producto>/', views.get_productos_finales, name='Ver Producto'),

    path('empresa/sucursal/<int:id_sucursal>/producto/<str:estado>/', views.get_productos_estado_by_sucursal, name='Lista Producto por Sucursal (activos o inactivos)'),
    path('empresa/sucursal/<int:id_sucursal>/producto/<str:estado>/producto/', views.get_productos_estado_productos_by_sucursal, name='Lista Producto por Sucursal (activos o inactivos) productos'),
    path('empresa/sucursal/<int:id_sucursal>/producto/<str:estado>/combo/', views.get_productos_estado_combos_by_sucursal, name='Lista Producto por Sucursal (activos o inactivos) combos'),
    # COMBO
    path('empresa/sucursal/combo/crear/', views.crear_combo, name='Crear Combo'),
    path('empresa/sucursal/combo/<int:id_combo>/editar/', views.editar_combo, name='Editar Combo'),
    # path('empresa/sucursal/combo/<int:id_combo>/ver/', views.getCombo, name='Ver Combo'),
    # path('empresa/sucursal/<int:id_sucursal>/combo/lista/', views.getCombos_by_sucursal, name='Lista de Combos por Sucursal'),
    # CATEGORIA
    path('empresa/categoria/lista/', views.getCategoria, name='Lista de Categorias Empresa'),
    # PEDIDO
    path('empresa/sucursal/pedido/crear/', views.crear_pedido, name='Crear Pedido - deprecado'),
    path('empresa/sucursal/pedido/crear_f/', views.crear_pedido_f, name='Crear Pedido'),
    path('empresa/sucursal/pedido/<int:id_pedido>/editar/', views.editar_pedido, name='Editar Pedido - Deprecado'),
    path('empresa/sucursal/pedido/<int:id_pedido>/editar_f/', views.editar_pedido_f, name='Editar Pedido'),
    path('empresa/sucursal/pedido/<int:id_pedido>/curso/', views.cambiar_pedido_en_curso, name='Cambiar pedido a en curso'),
    path('empresa/sucursal/pedido/<int:id_pedido>/finalizado/', views.cambiar_pedido_en_finalizado, name='Cambiar pedido a finalizado'),
    path('empresa/sucursal/pedido/<int:id_pedido>/cancelar/', views.cambiar_pedido_en_cancelado, name='Cambiar pedido a cancelado'),
    path('empresa/sucursal/pedido/<int:id_pedido>/cliente_finalizado/', views.cambiar_pedido_en_finalizado_cliente, name='Cambiar pedido a finalizado-cliente'),
    
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/', views.get_pedidos_by_sucursal, name='Lista de Pedidos por Sucursal'),
    path('empresa/<int:id_empresa>/sucursal/pedido/<str:estado>/', views.get_pedidos_by_empresa, name='Lista de Pedidos por Empresa'),
    path('empresa/sucursal/<int:id_sucursal>/pedido/<str:estado>/todo/', views.get_todos_pedidos_by_sucursal, name='Lista de Pedidos por Sucursal'),
    path('empresa/sucursal/pedido/<str:estado>/cliente/lista/', views.get_pedidos_by_estado_cliente, name='Lista de Pedidos por estado Cliente'),
    path('empresa/sucursal/pedido/cliente/activos/', views.get_pedidos_activos_by_cliente, name='Lista de Pedidos Activos por Cliente'),
    path('empresa/sucursal/pedido/cliente/finalizados/', views.get_pedidos_finalizados_by_cliente, name='Lista de Pedidos Finalizados por Cliente'),

    # path('empresa/sucursal/<int:id_sucursal>/pedido/lista/inactivos/', views.get_pedidos_by_sucursal_inactivos, name='Lista de Pedidos por sucursal Inactivos'),
    # path('empresa/sucursal/<int:id_sucursal>/pedido/lista/curso/', views.get_pedidos_by_sucursal_espera, name='Lista de Pedidos por sucursal en Curso'),
    path('empresa/sucursal/pedido/<int:id_pedido>/', views.ver_pedido, name='Ver Pedido'),
    # path('empresa/sucursal/<int:id_sucursal>/pedido/', views.get_pedidos, name='getPedidos'),
    path('test/', views.getp, name='V'),
    # PRODUCTO FINAL
    
    
    
    # path('empresa/sucursal/producto/editar/<int:id_producto>/', views.editar_producto, name='ModificarProducto'),
]