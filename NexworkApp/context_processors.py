from .models import SolicitudAmistad

def layout_context(request):
    if request.user.is_authenticated:
        solicitudes_pendientes = SolicitudAmistad.objects.filter(
            para_usuario=request.user,
            estado='pendiente'
        ).count()
    else:
        solicitudes_pendientes = 0

    return {
        'solicitudes_pendientes': solicitudes_pendientes
    }
