from django.contrib import admin

from .models import Producto


admin.site.site_header = 'FerroCasa (Admin)'
admin.site.site_title = 'FerroCasa (Admin)'
admin.site.index_title = 'Administración de FerroCasa'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria')
    list_editable = ('precio', 'stock')