import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from gestion.models import Categoria, Producto, Sucursal, Empleado, Inventario

LOTE = 5000  # filas por insercion; evita insertar de a una


class Command(BaseCommand):
    help = 'Carga datos ficticios con Faker. Uso: python manage.py poblar_datos 1000'

    def add_arguments(self, parser):
        parser.add_argument('cantidad', type=int, help='Cantidad de productos y empleados a crear')
        parser.add_argument('--limpiar', action='store_true', help='Borra los datos antes de cargar')

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        fake = Faker('es_CL')
        Faker.seed(42)
        random.seed(42)

        if options['limpiar']:
            Inventario.objects.all().delete()
            Empleado.objects.all().delete()
            Producto.objects.all().delete()
            Sucursal.objects.all().delete()
            Categoria.objects.all().delete()
            self.stdout.write('Datos anteriores eliminados.')

        # 1) Categorias (pocas)
        nombres_cat = ['Guitarras', 'Bajos', 'Baterias', 'Teclados', 'Vientos',
                       'Cuerdas', 'Accesorios', 'Audio', 'Amplificadores', 'Percusion']
        for n in nombres_cat:
            Categoria.objects.get_or_create(nombre=n, defaults={'descripcion': fake.sentence()})
        categorias = list(Categoria.objects.all())

        # 2) Sucursales (20)
        if Sucursal.objects.count() < 20:
            sucursales_nuevas = [
                Sucursal(
                    nombre=f'Sucursal {fake.city()} {i}',
                    direccion=fake.address(),
                    ciudad=fake.city(),
                    telefono=fake.phone_number()[:20],
                    fecha_apertura=fake.date_between(start_date='-10y', end_date='today'),
                    activo=random.choice([True, True, True, False]),
                )
                for i in range(20)
            ]
            Sucursal.objects.bulk_create(sucursales_nuevas)
        sucursales = list(Sucursal.objects.all())

        # 3) Productos (sku unico usando un contador)
        base = Producto.objects.count()
        self.stdout.write(f'Creando {cantidad} productos...')
        creados = 0
        while creados < cantidad:
            n = min(LOTE, cantidad - creados)
            lote = [
                Producto(
                    nombre=fake.word().capitalize() + ' ' + fake.word(),
                    sku=f'SKU-{base + creados + i:09d}',
                    precio=random.randint(1000, 2000000),
                    descripcion=fake.sentence(),
                    categoria=random.choice(categorias),
                )
                for i in range(n)
            ]
            Producto.objects.bulk_create(lote)
            creados += n
            self.stdout.write(f'  productos: {creados}/{cantidad}')

        # 4) Empleados (rut y email unicos usando un contador)
        base_emp = Empleado.objects.count()
        cargos = ['Vendedor', 'Cajero', 'Bodeguero', 'Supervisor', 'Gerente', 'Tecnico']
        self.stdout.write(f'Creando {cantidad} empleados...')
        creados = 0
        while creados < cantidad:
            n = min(LOTE, cantidad - creados)
            lote = []
            for i in range(n):
                k = base_emp + creados + i
                lote.append(Empleado(
                    nombre=fake.first_name(),
                    apellido=fake.last_name(),
                    rut=f'{10000000 + k}-{k % 10}',
                    email=f'empleado{k}@sucursal.cl',
                    cargo=random.choice(cargos),
                    sueldo=random.randint(450000, 3000000),
                    fecha_ingreso=fake.date_between(start_date='-8y', end_date='today'),
                    sucursal=random.choice(sucursales),
                ))
            Empleado.objects.bulk_create(lote)
            creados += n
            self.stdout.write(f'  empleados: {creados}/{cantidad}')

        # 5) Inventario: un producto por sucursal, sin repetir la pareja
        self.stdout.write('Creando inventarios...')
        ids_productos = list(Producto.objects.values_list('id', flat=True))
        existentes = set(Inventario.objects.values_list('sucursal_id', 'producto_id'))
        ahora = timezone.now()
        lote = []
        total = 0
        for pid in ids_productos:
            for suc in random.sample(sucursales, k=min(3, len(sucursales))):
                if (suc.id, pid) in existentes:
                    continue
                lote.append(Inventario(
                    stock=random.randint(0, 500),
                    fecha_actualizacion=ahora - timedelta(days=random.randint(0, 365)),
                    sucursal=suc,
                    producto_id=pid,
                ))
                if len(lote) >= LOTE:
                    Inventario.objects.bulk_create(lote)
                    total += len(lote)
                    lote = []
        if lote:
            Inventario.objects.bulk_create(lote)
            total += len(lote)

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {cantidad} productos, {cantidad} empleados y {total} inventarios.'
        ))