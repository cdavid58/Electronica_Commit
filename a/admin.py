from django.contrib import admin
from .models import *

class PostImageAdmin(admin.StackedInline):
    model = Imagenes

@admin.register(Articulo)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
       model = Articulo

@admin.register(Imagenes)
class PostImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tamanio)
admin.site.register(Color)
admin.site.register(Marca)
admin.site.register(Categoria)

admin.site.register(Consecutive)
admin.site.register(Client)
admin.site.register(Order)
