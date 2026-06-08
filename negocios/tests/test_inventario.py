


from django.test import TestCase
from negocios.models import (
    Negocio, Cliente, Insumo, Inventario,
    Producto, RecetaProducto, Categoria
)
from negocios.services.venta_service import crear_venta


class VentaServiceTest(TestCase):

    def setUp(self):
        self.negocio = Negocio.objects.create(
            nombre="Test",
            direccion="Test",
            comuna="Test",
            telefono="123",
            tipo_negocio="CARRO",
            margen=70
        )

        self.cliente = Cliente.objects.create(
            negocio=self.negocio,
            nombre="Cliente Test"
        )

        self.insumo = Insumo.objects.create(
            negocio=self.negocio,
            nombre="Manjar",
            unidad_medida="GR",
            costo_unitario=5
        )

        self.inventario = Inventario.objects.create(
            insumo=self.insumo,
            stock_actual=1000
        )

        self.categoria = Categoria.objects.create(
            negocio=self.negocio,
            nombre="Churros"
        )

        self.producto = Producto.objects.create(
            negocio=self.negocio,
            categoria=self.categoria,
            tipo="P",
            nombre="Churro",
            precio_venta=1000
        )

        RecetaProducto.objects.create(
            producto=self.producto,
            insumo=self.insumo,
            cantidad=50
        )

    def test_crear_venta_ok(self):

        venta = crear_venta(
            negocio=self.negocio,
            cliente=self.cliente,
            items=[
                {"producto": self.producto, "cantidad": 2}
            ]
        )

        self.insumo.refresh_from_db()
        self.assertEqual(venta.total, 2000)
        self.assertEqual(venta.detalle.count(), 1)
        self.assertEqual(self.insumo.inventario.stock_actual, 900)

    def test_venta_sin_stock(self):

        with self.assertRaises(Exception):
            crear_venta(
                negocio=self.negocio,
                cliente=self.cliente,
                items=[
                    {"producto": self.producto, "cantidad": 100}
                ]
            )