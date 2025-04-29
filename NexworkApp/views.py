from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Publicacion
from django.core.serializers import serialize
from django.utils.dateformat import DateFormat
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.templatetags.static import static
from django.utils.timezone import now
from .models import Usuario
from .models import Publicacion, Amistad, Like, Comentario
import json
from django.db.models import Q
import base64
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home_view(request):
    return render(request, 'Nexwork/index.html') 

def login_view(request):
    return render(request, 'Nexwork/auth/login.html') 

@csrf_exempt
def login_auth(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario = data.get('usuario')
        password = data.get('password')

        user = authenticate(request, usuario=usuario, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Inicio de sesión exitoso'})
        else:
            return JsonResponse({'success': False, 'message': 'Usuario o contraseña incorrectos'})

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

def publicaciones_publicas(request):
    usuario = request.user
    user_id = request.GET.get('id')

    if user_id:
        publicaciones = Publicacion.objects.select_related('autor') \
            .filter(autor_id=user_id) \
            .order_by('-fecha_creacion')
    else:
        amistades = Amistad.objects.filter(Q(usuario1=usuario) | Q(usuario2=usuario))
        amigos_ids = set()
        for amistad in amistades:
            if amistad.usuario1_id == usuario.id:
                amigos_ids.add(amistad.usuario2_id)
            else:
                amigos_ids.add(amistad.usuario1_id)

        amigos_ids.add(usuario.id)

        publicaciones = Publicacion.objects.select_related('autor') \
            .filter(autor_id__in=amigos_ids) \
            .order_by('-fecha_creacion')

    data = []

    for pub in publicaciones:
        imagen_base64 = None
        if pub.imagen:
            imagen_base64 = f"data:image/jpeg;base64,{base64.b64encode(pub.imagen).decode()}"
        
        if pub.autor.img_profile:
            img_profile = f"data:image/jpeg;base64,{base64.b64encode(pub.autor.img_profile).decode()}"
        else:
            img_profile = static('images/Nexwork/default-profile.png')

        # NUEVO: calcular like y likes count
        ya_dio_like = Like.objects.filter(usuario=usuario, publicacion=pub).exists()
        likes_count = pub.likes.count()

        # NUEVO: obtener nombres de usuarios que dieron like
        usuarios_like = list(pub.likes.all().values_list('usuario__nombre', flat=True)[:3])

        # NUEVO: contar comentarios
        comentarios_count = pub.comentarios.count()

        ahora = now()
        diferencia = ahora - pub.fecha_creacion

        if diferencia.total_seconds() < 60:
            fecha_formateada = "Hace un momento"
        elif diferencia.total_seconds() < 3600:
            minutos = int(diferencia.total_seconds() // 60)
            fecha_formateada = f"Hace {minutos} minuto{'s' if minutos != 1 else ''}"
        elif diferencia.total_seconds() < 86400:
            horas = int(diferencia.total_seconds() // 3600)
            fecha_formateada = f"Hace {horas} hora{'s' if horas != 1 else ''}"
        elif diferencia.total_seconds() < 604800:
            dias = int(diferencia.total_seconds() // 86400)
            fecha_formateada = f"Hace {dias} día{'s' if dias != 1 else ''}"
        elif diferencia.total_seconds() < 2592000:
            semanas = int(diferencia.total_seconds() // 604800)
            fecha_formateada = f"Hace {semanas} semana{'s' if semanas != 1 else ''}"
        else:
            fecha_formateada = DateFormat(pub.fecha_creacion).format('d M Y H:i')

        data.append({
            'id': pub.id,
            'autor_id': pub.autor.id,
            'autor': pub.autor.usuario,
            'nombre': f"{pub.autor.nombre} {pub.autor.apellidos}",
            'fecha': fecha_formateada,
            'descripcion': pub.descripcion,
            'imagen': imagen_base64,
            'img_profile': img_profile,
            'es_mia': pub.autor_id == usuario.id,
            'ya_dio_like': ya_dio_like,
            'likes_count': likes_count,
            'usuarios_like': usuarios_like,
            'comentarios_count': comentarios_count,
        })

    return JsonResponse({'publicaciones': data})

@csrf_exempt
@require_POST
def editar_publicacion(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)

    try:
        pub = Publicacion.objects.get(id=id, autor=request.user)
    except Publicacion.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

    descripcion = request.POST.get('descripcion', '').strip()
    imagen = request.FILES.get('imagen')
    borrar_imagen = request.POST.get('borrar_imagen') == 'true'

    pub.descripcion = descripcion

    if borrar_imagen:
        pub.imagen = None  # Limpia la imagen
    elif imagen:
        pub.imagen = imagen.read()

    pub.save()

    return JsonResponse({'success': True})

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_publicacion(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)

    try:
        pub = Publicacion.objects.get(id=id, autor=request.user)
        pub.delete()
        return JsonResponse({'success': True})
    except Publicacion.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'No encontrada'}, status=404)

@csrf_exempt
def nueva_publicacion(request):
    if request.method == 'POST' and request.user.is_authenticated:
        descripcion = request.POST.get('descripcion')
        es_publico = request.POST.get('es_publico') == 'true'
        imagen = request.FILES.get('imagen')

        imagen_bytes = imagen.read() if imagen else None

        Publicacion.objects.create(
            autor=request.user,
            descripcion=descripcion,
            es_publico=es_publico,
            imagen=imagen_bytes
        )
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def toggle_like_publicacion(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)

    try:
        publicacion = Publicacion.objects.get(id=id)
    except Publicacion.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Publicación no encontrada'}, status=404)

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(usuario=request.user, publicacion=publicacion)
        return JsonResponse({'success': created, 'liked': True})

    if request.method == 'DELETE':
        Like.objects.filter(usuario=request.user, publicacion=publicacion).delete()
        return JsonResponse({'success': True, 'liked': False})

def obtener_comentarios(request, publicacion_id):
    comentarios = Comentario.objects.select_related('autor').filter(publicacion_id=publicacion_id).order_by('-fecha_creacion')
    ahora = now()

    data = []
    for comentario in comentarios:
        if comentario.autor.img_profile:
            img_profile = f"data:image/jpeg;base64,{base64.b64encode(comentario.autor.img_profile).decode()}"
        else:
            img_profile = static('images/Nexwork/default-profile.png')

        # Calcular diferencia de tiempo
        diferencia = ahora - comentario.fecha_creacion

        if diferencia.total_seconds() < 60:
            fecha_formateada = "Hace un momento"
        elif diferencia.total_seconds() < 3600:
            minutos = int(diferencia.total_seconds() // 60)
            fecha_formateada = f"Hace {minutos} minuto{'s' if minutos != 1 else ''}"
        elif diferencia.total_seconds() < 86400:
            horas = int(diferencia.total_seconds() // 3600)
            fecha_formateada = f"Hace {horas} hora{'s' if horas != 1 else ''}"
        elif diferencia.total_seconds() < 604800:
            dias = int(diferencia.total_seconds() // 86400)
            fecha_formateada = f"Hace {dias} día{'s' if dias != 1 else ''}"
        elif diferencia.total_seconds() < 2592000:
            semanas = int(diferencia.total_seconds() // 604800)
            fecha_formateada = f"Hace {semanas} semana{'s' if semanas != 1 else ''}"
        else:
            fecha_formateada = DateFormat(comentario.fecha_creacion).format('d M Y H:i')

        data.append({
            'comentario_id': comentario.id,
            'autor': f"{comentario.autor.nombre} {comentario.autor.apellidos}",
            'contenido': comentario.contenido,
            'fecha': fecha_formateada,
            'img_profile': img_profile,
            'es_mio': comentario.autor_id == request.user.id,
        })

    return JsonResponse({'comentarios': data})

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_comentario(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)

    try:
        comentario = Comentario.objects.get(id=id, autor=request.user)
        comentario.delete()
        return JsonResponse({'success': True})
    except Comentario.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Comentario no encontrado'}, status=404)

@csrf_exempt
@require_POST
def editar_comentario(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)

    try:
        comentario = Comentario.objects.get(id=id, autor=request.user)
        data = json.loads(request.body)
        contenido = data.get('contenido', '').strip()

        if not contenido:
            return JsonResponse({'success': False, 'message': 'Comentario vacío'}, status=400)

        comentario.contenido = contenido
        comentario.save()

        return JsonResponse({'success': True, 'publicacion_id': comentario.publicacion_id})
    except Comentario.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Comentario no encontrado'}, status=404)

@csrf_exempt
@require_POST
def nuevo_comentario(request, publicacion_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)

    try:
        data = json.loads(request.body)
        contenido = data.get('contenido', '').strip()

        if not contenido:
            return JsonResponse({'success': False, 'message': 'Comentario vacío'}, status=400)

        publicacion = Publicacion.objects.get(id=publicacion_id)
        Comentario.objects.create(
            publicacion=publicacion,
            autor=request.user,
            contenido=contenido
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

def profile_view(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    # Imagen de perfil
    if usuario.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    # Banner del perfil
    if usuario.banner_profile:
        banner_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.banner_profile).decode()}"
    else:
        banner_profile = static('images/Nexwork/banner_default2.png')

    return render(request, 'Nexwork/profile.html', {
        'usuario': usuario,
        'img_profile': img_profile,
        'banner_profile': banner_profile,
    })

@csrf_exempt
@require_POST
def actualizar_img_profile(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.user != usuario:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    imagen = request.FILES.get('imagen')
    if imagen:
        usuario.img_profile = imagen.read()
        usuario.save()
        imagen_base64 = f"data:image/jpeg;base64,{base64.b64encode(usuario.img_profile).decode()}"
        return JsonResponse({'success': True, 'img_profile': imagen_base64})

    return JsonResponse({'success': False, 'error': 'No se envió imagen'}, status=400)

@csrf_exempt
@require_POST
def actualizar_banner_profile(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.user != usuario:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    banner = request.FILES.get('imagen')
    if banner:
        usuario.banner_profile = banner.read()
        usuario.save()
        banner_base64 = f"data:image/jpeg;base64,{base64.b64encode(usuario.banner_profile).decode()}"
        return JsonResponse({'success': True, 'banner_profile': banner_base64})

    return JsonResponse({'success': False, 'error': 'No se envió banner'}, status=400)
