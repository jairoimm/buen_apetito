from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from negocios.models import Producto, Cliente, Negocio
from negocios.services.venta_service import crear_venta
from .serializers import VentaCreateSerializer

class CrearVentaAPIView(APIView):

    def post(self, request):

        serializer = VentaCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        negocio = Negocio.objects.first()  # luego lo mejoramos
        cliente = None

        if "cliente_id" in data:
            cliente = Cliente.objects.get(id=data["cliente_id"])

        items = []

        for item in data["items"]:
            producto = Producto.objects.get(id=item["producto_id"])

            items.append({
                "producto": producto,
                "cantidad": item["cantidad"]
            })

        venta = crear_venta(
            negocio=negocio,
            cliente=cliente,
            items=items
        )

        return Response({
            "mensaje": "Venta creada correctamente",
            "venta_id": venta.id,
            "total": venta.total
        }, status=status.HTTP_201_CREATED)