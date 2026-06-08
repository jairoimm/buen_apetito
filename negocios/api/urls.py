from django.urls import path
from .views import CrearVentaAPIView

urlpatterns = [
    path('ventas/', CrearVentaAPIView.as_view(), name='crear-venta'),
]