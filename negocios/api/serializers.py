from rest_framework import serializers
from negocios.models import Venta, DetalleVenta, Producto


class DetalleVentaSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=12, decimal_places=3)


class VentaCreateSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField(required=False)
    items = DetalleVentaSerializer(many=True)