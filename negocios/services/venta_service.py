from django.db import transaction
from django.core.exceptions import ValidationError
from negocios.models import Venta, DetalleVenta, MovimientoInventario, SecuenciaVenta


@transaction.atomic
def crear_venta(negocio, cliente, items):

    if not items:
        raise ValidationError("La venta no tiene productos")

    total = 0

    numero = generar_numero_venta(negocio)

    venta = Venta.objects.create(
        negocio=negocio,
        cliente=cliente,
        numero=numero,
        total=0
    )

    for item in items:
        producto = item["producto"]
        cantidad = item["cantidad"]

        if cantidad <= 0:
            raise ValidationError("Cantidad inválida")

        detalle = DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio_venta
        )

        total += detalle.subtotal

        for receta in producto.recetas.all():

            inventario = getattr(receta.insumo, "inventario", None)

            if not inventario:
                raise ValidationError(f"No hay inventario para {receta.insumo.nombre}")

            if inventario.stock_disponible < (receta.cantidad * cantidad):
                raise ValidationError(f"No hay suficiente {receta.insumo.nombre}")

            MovimientoInventario.objects.create(
                insumo=receta.insumo,
                tipo="VENTA",
                cantidad=-(receta.cantidad * cantidad),
                referencia=f"Venta {venta.numero}"
            )

    venta.total = total
    venta.save()

    return venta


def generar_numero_venta(negocio):

    secuencia, _ = SecuenciaVenta.objects.select_for_update().get_or_create(
        negocio=negocio
    )

    secuencia.ultimo_numero += 1
    secuencia.save()

    return f"V-{secuencia.ultimo_numero:04d}"