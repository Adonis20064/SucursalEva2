from django.db import models

# Create your models here.

#modelos categorias
class Categoria(models.Model): 
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    sku= models.CharField(max_length=50, unique=True) #el sku es indendificador unico de cada producto.
    precio = models.PositiveIntegerField() #el precio es un entero positivo
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, #foren key y con una proteccion para que no se pueda eliminar una categoria si tiene productos asociados
                                on_delete=models.PROTECT,
                                related_name='productos'
    )
    
    
    def __str__(self):
        return f'{self.nombre} ({self.sku})'

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_apertura = models.DateField()
    activo = models.BooleanField(default=True) #Si la sucursal esta activa o no
    
    class Meta:
        verbose_name_plural = "Sucursales" #para que en el admin de django se vea Sucursales en vez de Sucursal
        ordering = ['nombre'] #para que en el admin de django se ordene por nombre

    def __str__(self):
        return f'{self.nombre} - {self.ciudad}'
    
    
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=100)
    sueldo = models.PositiveIntegerField() #el sueldo es un entero positivo
    fecha_ingreso = models.DateField()
    sucursal = models.ForeignKey(Sucursal, #foren key y con una proteccion para que no se pueda eliminar una sucursal si tiene empleados asociados
                                on_delete=models.PROTECT,
                                related_name='empleados'
    )
    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.sucursal.nombre}'
    
    
class Inventario(models.Model):
    stock = models.PositiveIntegerField(default=0) #el stock es un entero positivo
    fecha_actualizacion = models.DateTimeField(auto_now=True) #auto_now para que se actualice automaticamente la fecha de actualizacion
    sucursal = models.ForeignKey(Sucursal,
                                    on_delete=models.CASCADE,
                                    related_name='inventarios')
    producto = models.ForeignKey(Producto,
                                    on_delete=models.CASCADE,
                                    related_name='inventarios')
    
    #Creamos la clase meta para decirle como debe comportarse el modelo y darle un nombre a la restriccion
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sucursal', 'producto'], name='unique_inventario', )
            
        ]
        

    def __str__(self):
        return f'{self.producto.nombre} - {self.sucursal.nombre} - Stock: {self.stock}'