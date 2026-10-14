from django.contrib import admin
from .models import Categoria, Producto, Sucursal, Empleado, Inventario


# Register your models here.
@admin.register(Categoria) #admin.register es un decorador que registra el modelo en el admin de django
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion') #list_display es una tupla que indica los campos que se van a mostrar en la lista de categorias
    search_fields = ('nombre',) #search_fields es una tupla que indica los campos por los que se puede buscar en la lista de categorias
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'precio', 'categoria')
    list_filter = ('categoria',) #list_filter es una tupla que indica los campos por los que se puede filtrar en la lista de productos
    search_fields = ('nombre', 'sku', 'categoria__nombre') # seach_field es una tupla que indica los campos por los que se puede buscar en la lista de productos, categoria__nombre es para buscar por el nombre de la categoria del producto
    list_select_related = ('categoria',) #list_select_related es una tupla que indica los campos por los que se puede hacer select_related en la lista de productos, categoria es para hacer select_related con la categoria del producto
    
@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'ciudad', 'telefono', 'fecha_apertura', 'activo')
    list_filter = ('activo', 'ciudad') #list_filter es una tupla que indica los campos por los que se puede filtrar en la lista de sucursales
    search_fields = ('nombre', 'ciudad') #search_fields es una tupla que indica los campos por los que se puede buscar en la lista de sucursales
    

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'rut', 'email', 'cargo', 'sueldo', 'fecha_ingreso', 'sucursal')
    list_filter = ('cargo', 'sucursal') #list_filter es una tupla que indica los campos por los que se puede filtrar en la lista de empleados
    search_fields = ('nombre', 'apellido', 'rut', 'email', 'cargo', 'sucursal__nombre') #search_fields es una tupla que indica los campos por los que se puede buscar en la lista de empleados, sucursal__nombre es para buscar por el nombre de la sucursal del empleado
    list_select_related = ('sucursal',) #list_select_related es una tupla que indica los campos por los que se puede hacer select_related en la lista de empleados, sucursal es para hacer select_related con la sucursal del empleado
    
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'producto', 'stock', 'fecha_actualizacion')
    list_filter = ('sucursal', 'producto') #list_filter es una tupla que indica los campos por los que se puede filtrar en la lista de inventarios
    search_fields = ('sucursal__nombre', 'producto__nombre') #search_fields es una tupla que indica los campos por los que se puede buscar en la lista de inventarios, sucursal__nombre y producto__nombre son para buscar por el nombre de la sucursal y del producto del inventario
    list_select_related = ('sucursal', 'producto') #list_select_related es una tupla que indica los campos por los que se puede hacer select_related en la lista de inventarios, sucursal y producto son para hacer select_related con la sucursal y el producto del inventario
    
    
    
#python manage.py poblar_datos 100 --limpiar
#python manage.py poblar_datos 1000 --limpiar
#python manage.py poblar_datos 100000 --limpiar
