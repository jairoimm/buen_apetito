from django.test import TestCase
from negocios.models import Insumo, Inventario, Negocio


class InventarioTest(TestCase):

    def test_stock_disponible(self):

        negocio = Negocio.objects.create(
            nombre="Test",
            direccion="Test",
            comuna="Test",
            telefono="123",
            tipo_negocio="CARRO",
            margen=70
        )

        insumo = Insumo.objects.create(
            negocio=negocio,
            nombre="Chocolate",
            unidad_medida="GR",
            costo_unitario=10
        )

        inventario = Inventario.objects.create(
            insumo=insumo,
            stock_actual=100,
            stock_reservado=20
        )

        self.assertEqual(inventario.stock_disponible, 80)