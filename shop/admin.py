from django.contrib import admin
from .models import Producto, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('nombre', 'precio', 'is_oferta')
    list_filter = ('is_oferta',)