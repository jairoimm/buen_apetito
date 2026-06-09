from rest_framework.permissions import BasePermission
from negocios.models import Negocio


class EsPropietarioDelNegocio(BasePermission):
    """
    Verifica que el negocio solicitado pertenezca al usuario autenticado.
    Requiere que la vista tenga self.negocio seteado.
    """
    message = "No tienes permiso para acceder a este negocio."

    def has_permission(self, request, view):
        negocio_id = view.kwargs.get('negocio_id')
        if not negocio_id:
            return False
        return Negocio.objects.filter(
            id=negocio_id,
            propietario=request.user,
            activo=True
        ).exists()
