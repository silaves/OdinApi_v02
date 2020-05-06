from django.conf import settings
from django.contrib import admin
from apps.empresa.models import Empresa, Sucursal, Pedido, Combo, Chat_Pedido, ProductoFinal, CategoriaEmpresa
from django.utils.safestring import mark_safe

class ProductoFinalAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.foto:
            print(settings.BASE_DIR+obj.foto.url)
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % (settings.BASE_DIR+obj.foto.url))
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
    list_display = ('nombre','id','precio','estado','sucursal','image_tag',)

# class Combo_inline(admin.StackedInline):
#     model = ComboProducto

# class ComboAdmin(admin.ModelAdmin):
#     inlines = [Combo_inline]

admin.site.register(Empresa)
admin.site.register(Sucursal)
# admin.site.register(Pedido)
# admin.site.register(Combo, ComboAdmin)
# admin.site.register(Chat_Pedido)
admin.site.register(CategoriaEmpresa)