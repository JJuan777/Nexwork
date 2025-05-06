from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Publicacion
from django.core.serializers import serialize
from django.utils.dateformat import DateFormat
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.templatetags.static import static
from django.contrib.auth import logout
from django.utils.timezone import now
from datetime import timedelta
from .models import Usuario
from .models import Publicacion, Amistad, Like, Comentario, PublicacionCompartida, SolicitudAmistad
from .models import ExperienciaLaboral, Educacion
from django.utils.dateparse import parse_date
from .models import Trabajo, Postulacion
import json
from django.db.models import Q
import base64, requests
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count
from .models import VistaTrabajo


# Create your views here.
@login_required
def home_view(request):
    trabajos = Trabajo.objects.filter(activo=True).select_related('autor').order_by('-fecha_publicacion')[:2]
    return render(request, 'Nexwork/index.html', {
        'trabajos_recientes': trabajos
    })

def login_view(request):
    return render(request, 'Nexwork/auth/login.html') 

def logout_view(request):
    logout(request)
    return redirect('login')

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

def formatear_fecha_relativa(fecha):
    diferencia = now() - fecha

    if diferencia.total_seconds() < 60:
        return "Hace un momento"
    elif diferencia.total_seconds() < 3600:
        minutos = int(diferencia.total_seconds() // 60)
        return f"Hace {minutos} minuto{'s' if minutos != 1 else ''}"
    elif diferencia.total_seconds() < 86400:
        horas = int(diferencia.total_seconds() // 3600)
        return f"Hace {horas} hora{'s' if horas != 1 else ''}"
    elif diferencia.total_seconds() < 604800:
        dias = int(diferencia.total_seconds() // 86400)
        return f"Hace {dias} día{'s' if dias != 1 else ''}"
    elif diferencia.total_seconds() < 2592000:
        semanas = int(diferencia.total_seconds() // 604800)
        return f"Hace {semanas} semana{'s' if semanas != 1 else ''}"
    else:
        return DateFormat(fecha).format('d M Y H:i')

def publicaciones_publicas(request):
    usuario = request.user
    user_id = request.GET.get('id')
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 5))

    publicaciones_data = []

    if user_id:
        publicaciones = Publicacion.objects.select_related('autor') \
            .filter(autor_id=user_id) \
            .order_by('-fecha_creacion')

        compartidas = PublicacionCompartida.objects.select_related('usuario', 'publicacion_original', 'publicacion_original__autor') \
            .filter(usuario_id=user_id, es_publico=True) \
            .order_by('-fecha_compartida')
    else:
        amistades = Amistad.objects.filter(Q(usuario1=usuario) | Q(usuario2=usuario))
        amigos_ids = {
            amistad.usuario2_id if amistad.usuario1_id == usuario.id else amistad.usuario1_id
            for amistad in amistades
        }
        amigos_ids.add(usuario.id)

        publicaciones = Publicacion.objects.select_related('autor') \
            .filter(autor_id__in=amigos_ids) \
            .order_by('-fecha_creacion')

        compartidas = PublicacionCompartida.objects.select_related('usuario', 'publicacion_original', 'publicacion_original__autor') \
            .filter(usuario_id__in=amigos_ids, es_publico=True) \
            .order_by('-fecha_compartida')

    # Combinar ambas listas y ordenarlas por fecha (fecha_creacion o fecha_compartida)
    items = [
        {"tipo": "original", "obj": p, "fecha": p.fecha_creacion} for p in publicaciones
    ] + [
        {"tipo": "compartida", "obj": pc, "fecha": pc.fecha_compartida} for pc in compartidas
    ]

    items.sort(key=lambda x: x['fecha'], reverse=True)
    items = items[offset:offset + limit]

    for item in items:
        if item['tipo'] == 'original':
            pub = item['obj']
            autor = pub.autor
        else:  # compartida
            pc = item['obj']
            pub = pc.publicacion_original
            autor = pc.usuario  # quien compartió

        imagen_base64 = (
            f"data:image/jpeg;base64,{base64.b64encode(pub.imagen).decode()}"
            if pub.imagen else None
        )

        img_profile_autor_original = (
            f"data:image/jpeg;base64,{base64.b64encode(pub.autor.img_profile).decode()}"
            if pub.autor.img_profile else static('images/Nexwork/default-profile.png')
        )

        img_profile_compartido_por = (
            f"data:image/jpeg;base64,{base64.b64encode(autor.img_profile).decode()}"
            if autor.img_profile else static('images/Nexwork/default-profile.png')
        )

        publicaciones_data.append({
            'id': pub.id,
            'autor_id': pub.autor.id,
            'autor': pub.autor.usuario,
            'nombre': f"{pub.autor.nombre} {pub.autor.apellidos}",
            'fecha': formatear_fecha_relativa(item['fecha']),
            'descripcion': pub.descripcion,
            'imagen': imagen_base64,
            'img_profile_autor_original': img_profile_autor_original,
            'img_profile_compartido_por': img_profile_compartido_por,
            'es_mia': pub.autor_id == usuario.id,
            'ya_dio_like': Like.objects.filter(usuario=usuario, publicacion=pub).exists(),
            'likes_count': pub.likes.count(),
            'usuarios_like': list(pub.likes.all().values_list('usuario__nombre', flat=True)[:3]),
            'comentarios_count': pub.comentarios.count(),
            'es_compartida': item['tipo'] == 'compartida',
            'compartido_por': f"{autor.nombre} {autor.apellidos}" if item['tipo'] == 'compartida' else None,
            'comentario_compartido': item['obj'].comentario if item['tipo'] == 'compartida' else None,
            'id_compartida': item['obj'].id if item['tipo'] == 'compartida' else None,
            'autor_compartida_id': autor.id if item['tipo'] == 'compartida' else None,

        })

    return JsonResponse({'publicaciones': publicaciones_data})

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
@require_http_methods(["DELETE"])
def eliminar_publicacion_compartida(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)

    try:
        pc = PublicacionCompartida.objects.get(id=id, usuario=request.user)
        pc.delete()
        return JsonResponse({'success': True})
    except PublicacionCompartida.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Publicación compartida no encontrada'}, status=404)

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
    actual = request.user

    # Imagen de perfil
    if usuario.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    # Banner
    if usuario.banner_profile:
        banner_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.banner_profile).decode()}"
    else:
        banner_profile = static('images/Nexwork/banner_default2.png')


    todas_experiencias = usuario.experiencias.order_by('-fecha_inicio')
    experiencias = todas_experiencias[:2]
    hay_mas_experiencias = todas_experiencias.count() > 2

    # Preprocesar tecnologías
    for exp in experiencias:
        if exp.tecnologias:
            exp.tecnologias_lista = [tag.strip() for tag in exp.tecnologias.split(',')]
        else:
            exp.tecnologias_lista = []

    # Cargar educación (máximo 2 registros)
    educaciones = usuario.educacion.all()[:2]
    hay_mas_educacion = usuario.educacion.count() > 2

    # Preprocesar áreas de estudio
    for edu in educaciones:
        if edu.areas_estudio:
            edu.areas_estudio_lista = [tag.strip() for tag in edu.areas_estudio.split(',')]
        else:
            edu.areas_estudio_lista = []


    # Inicializar variables
    ya_son_amigos = False
    solicitud_pendiente = False
    contactos = []

    if actual.is_authenticated:
        # Verificar estado de amistad si es otro perfil
        if actual != usuario:
            ya_son_amigos = Amistad.objects.filter(
                Q(usuario1=actual, usuario2=usuario) |
                Q(usuario1=usuario, usuario2=actual)
            ).exists()

            solicitud_pendiente = SolicitudAmistad.objects.filter(
                de_usuario=actual,
                para_usuario=usuario,
                estado='pendiente'
            ).exists()

        # Obtener contactos del usuario visitado (máximo 5)
        amistades = Amistad.objects.filter(Q(usuario1=usuario) | Q(usuario2=usuario))[:5]
        contactos = [
            a.usuario2 if a.usuario1 == usuario else a.usuario1
            for a in amistades
        ]

    return render(request, 'Nexwork/profile.html', {
        'usuario': usuario,
        'img_profile': img_profile,
        'banner_profile': banner_profile,
        'ya_son_amigos': ya_son_amigos,
        'solicitud_pendiente': solicitud_pendiente,
        'contactos': contactos,
        'experiencias': experiencias,
        'hay_mas_experiencias': hay_mas_experiencias,
        'educaciones': educaciones,
        'hay_mas_educacion': hay_mas_educacion,

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

@require_POST
@login_required
def compartir_publicacion(request):
    publicacion_id = request.POST.get('publicacion_id')
    comentario = request.POST.get('comentario', '').strip()
    es_publico = request.POST.get('es_publico') == 'true'

    try:
        original = Publicacion.objects.get(pk=publicacion_id)
        PublicacionCompartida.objects.create(
            usuario=request.user,
            publicacion_original=original,
            comentario=comentario,
            es_publico=es_publico
        )
        return JsonResponse({'success': True})
    except Publicacion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Publicación no encontrada'})

@require_POST
@login_required
def enviar_solicitud_amistad(request):
    data = json.loads(request.body)
    para_usuario_id = data.get('para_usuario_id')

    if not para_usuario_id or int(para_usuario_id) == request.user.id:
        return JsonResponse({'success': False, 'message': 'Solicitud inválida'})

    try:
        para_usuario = Usuario.objects.get(id=para_usuario_id)

        if Amistad.objects.filter(
            Q(usuario1=request.user, usuario2=para_usuario) |
            Q(usuario1=para_usuario, usuario2=request.user)
        ).exists():
            return JsonResponse({'success': False, 'message': 'Ya son amigos'})

        SolicitudAmistad.objects.get_or_create(
            de_usuario=request.user,
            para_usuario=para_usuario,
            defaults={'estado': 'pendiente'}
        )

        return JsonResponse({'success': True})

    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})

def experiencias_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if usuario.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    return render(request, 'Nexwork/experiencias.html', {
        'usuario': usuario,
        'img_profile': img_profile
    })

def api_experiencias_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    experiencias = usuario.experiencias.order_by('-fecha_inicio')

    datos = []
    for exp in experiencias:
        tecnologias = [tag.strip() for tag in exp.tecnologias.split(',')] if exp.tecnologias else []
        datos.append({
            'id': exp.id, 
            'puesto': exp.puesto,
            'empresa': exp.empresa,
            'fecha_inicio': exp.fecha_inicio.strftime('%b %Y'),
            'fecha_fin': exp.fecha_fin.strftime('%Y') if exp.fecha_fin else 'Presente',
            'tecnologias': tecnologias,
            'descripcion': exp.descripcion or ""
        })

    return JsonResponse({'experiencias': datos})

@csrf_exempt
@require_POST
def actualizar_experiencia(request, id):
    try:
        experiencia = ExperienciaLaboral.objects.get(id=id)
        if experiencia.usuario != request.user:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

        data = json.loads(request.body)

        # Validar que fecha_inicio esté presente
        fecha_inicio = data.get('fecha_inicio')
        if not fecha_inicio:
            return JsonResponse({'success': False, 'error': 'La fecha de inicio es obligatoria.'}, status=400)

        fecha_fin = data.get('fecha_fin')

        experiencia.puesto = data.get('puesto', experiencia.puesto)
        experiencia.empresa = data.get('empresa', experiencia.empresa)
        experiencia.descripcion = data.get('descripcion', experiencia.descripcion)
        experiencia.fecha_inicio = parse_date(fecha_inicio)
        experiencia.fecha_fin = parse_date(fecha_fin) if fecha_fin else None

        # Validar tecnologías
        tecnologias = data.get('tecnologias', [])
        if len(tecnologias) > 5:
            return JsonResponse({'success': False, 'error': 'Máximo 5 tecnologías permitidas.'}, status=400)

        experiencia.tecnologias = ", ".join(tecnologias)
        experiencia.save()

        return JsonResponse({'success': True})

    except ExperienciaLaboral.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Experiencia no encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def nueva_experiencia(request, id):
    try:
        usuario = get_object_or_404(Usuario, id=id)
        if usuario != request.user:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

        data = json.loads(request.body)

        if not data.get('fecha_inicio'):
            return JsonResponse({'success': False, 'error': 'Fecha de inicio obligatoria'}, status=400)

        tecnologias = data.get('tecnologias', [])
        if len(tecnologias) > 5:
            return JsonResponse({'success': False, 'error': 'Máximo 5 tecnologías'}, status=400)

        ExperienciaLaboral.objects.create(
            usuario=usuario,
            puesto=data.get('puesto'),
            empresa=data.get('empresa'),
            fecha_inicio=parse_date(data.get('fecha_inicio')),
            fecha_fin=parse_date(data.get('fecha_fin')) if data.get('fecha_fin') else None,
            descripcion=data.get('descripcion', ''),
            tecnologias=", ".join(tecnologias)
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_experiencia(request, id):
    try:
        experiencia = ExperienciaLaboral.objects.get(id=id)
        if experiencia.usuario != request.user:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
        experiencia.delete()
        return JsonResponse({'success': True})
    except ExperienciaLaboral.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Experiencia no encontrada'}, status=404)

def educacion_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    if usuario.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    return render(request, 'Nexwork/educacion.html', {
        'usuario': usuario,
        'img_profile': img_profile
    })

def api_educacion_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    educaciones = usuario.educacion.all()  # ← correcto uso del related_name

    data = []
    for edu in educaciones:
        areas = [tag.strip() for tag in edu.areas_estudio.split(',')] if edu.areas_estudio else []
        data.append({
            'id': edu.id,
            'titulo': edu.titulo,
            'institucion': edu.institucion,
            'fecha_inicio': edu.fecha_inicio.strftime('%Y'),
            'fecha_fin': edu.fecha_fin.strftime('%Y') if edu.fecha_fin else 'Presente',
            'areas': areas
        })

    return JsonResponse({'educaciones': data})

@csrf_exempt
@require_POST
def actualizar_educacion(request, id):
    try:
        educacion = Educacion.objects.get(id=id)
        if educacion.usuario != request.user:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

        data = json.loads(request.body)
        educacion.titulo = data.get('titulo', educacion.titulo)
        educacion.institucion = data.get('institucion', educacion.institucion)

        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if fecha_inicio:
            educacion.fecha_inicio = parse_date(fecha_inicio)
        if fecha_fin:
            educacion.fecha_fin = parse_date(fecha_fin)
        else:
            educacion.fecha_fin = None

        areas = data.get('areas', [])
        if len(areas) > 5:
            return JsonResponse({'success': False, 'error': 'Máximo 5 áreas de estudio'}, status=400)
        educacion.areas_estudio = ', '.join(areas)

        educacion.save()
        return JsonResponse({'success': True})

    except Educacion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No existe'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(['DELETE'])
def eliminar_educacion(request, id):
    try:
        educacion = Educacion.objects.get(id=id)
        if educacion.usuario != request.user:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
        educacion.delete()
        return JsonResponse({'success': True})
    except Educacion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No existe'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@csrf_exempt
@require_POST
def crear_educacion(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
        if usuario != request.user:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

        data = json.loads(request.body)
        titulo = data.get('titulo')
        institucion = data.get('institucion')
        fecha_inicio = parse_date(data.get('fecha_inicio'))
        fecha_fin = parse_date(data.get('fecha_fin')) if data.get('fecha_fin') else None
        areas = [a.strip() for a in data.get('areas_estudio', '').split(',') if a.strip()]
        if len(areas) > 5:
            return JsonResponse({'success': False, 'error': 'Máximo 5 áreas de estudio'}, status=400)

        Educacion.objects.create(
            usuario=usuario,
            titulo=titulo,
            institucion=institucion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            areas_estudio=", ".join(areas)
        )

        return JsonResponse({'success': True})

    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def trabajos_view(request):
    return render(request, 'Nexwork/trabajos.html') 

@login_required
def trabajos_api(request):
    query = request.GET.get('q', '').strip()
    ubicacion = request.GET.get('ubicacion', '').strip()
    modalidad = request.GET.get('modalidad', '').strip()

    trabajos = Trabajo.objects.select_related('autor').filter(activo=True)

    if query:
        trabajos = trabajos.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )
    if ubicacion:
        trabajos = trabajos.filter(ubicacion__icontains=ubicacion)
    if modalidad:
        trabajos = trabajos.filter(modalidad=modalidad)

    trabajos = trabajos.order_by('-fecha_publicacion')

    usuario = request.user
    postulaciones = set(
        Postulacion.objects.filter(usuario=usuario).values_list('trabajo_id', flat=True)
    )

    data = []
    for t in trabajos:
        if t.autor.img_profile:
            img_profile = f"data:image/jpeg;base64,{base64.b64encode(t.autor.img_profile).decode()}"
        else:
            img_profile = static('images/Nexwork/default-profile.png')

        data.append({
            'id': t.id,
            'titulo': t.titulo,
            'descripcion': t.descripcion[:150] + ("..." if len(t.descripcion) > 150 else ""),
            'ubicacion': t.ubicacion,
            'modalidad': t.modalidad.title(),
            'fecha': formatear_fecha_relativa(t.fecha_publicacion),
            'autor_id': t.autor.id,
            'autor_nombre': f"{t.autor.nombre} {t.autor.apellidos}",
            'img_profile': img_profile,
            'ya_postulado': t.id in postulaciones,
        })

    return JsonResponse({'trabajos': data})

@csrf_exempt
@require_POST
def postularse_trabajo(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)

    trabajo = get_object_or_404(Trabajo, id=id)

    # Verificar si ya se postuló
    if Postulacion.objects.filter(trabajo=trabajo, usuario=request.user).exists():
        return JsonResponse({'success': False, 'error': 'Ya te has postulado a este trabajo'}, status=400)

    try:
        data = json.loads(request.body)
        mensaje = data.get('mensaje', '').strip()

        Postulacion.objects.create(
            trabajo=trabajo,
            usuario=request.user,
            mensaje=mensaje,
            fecha_postulacion=now()
        )

        return JsonResponse({'success': True, 'message': 'Postulación enviada correctamente'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def geolocalizar_ip(ip):
    """Consulta geolocalización básica por IP"""
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        if response.status_code == 200:
            data = response.json()
            return {
                'ciudad': data.get('city'),
                'estado': data.get('region'),
                'pais': data.get('country_name'),
            }
    except:
        pass
    return {'ciudad': None, 'estado': None, 'pais': None}


@login_required
def trabajo_detalle_view(request, id):
    trabajo = get_object_or_404(Trabajo.objects.select_related('autor'), pk=id, activo=True)

    if trabajo.autor.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(trabajo.autor.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    ya_postulado = Postulacion.objects.filter(trabajo=trabajo, usuario=request.user).exists()

    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # ⚠️ Evita múltiples registros en ventana de 30 min
    ventana = now() - timedelta(minutes=30)
    ya_existe = VistaTrabajo.objects.filter(
        trabajo=trabajo,
        usuario=request.user,
        ip=ip,
        fecha__gte=ventana
    ).exists()

    if not ya_existe:
        geo = geolocalizar_ip(ip)
        VistaTrabajo.objects.create(
            trabajo=trabajo,
            usuario=request.user,
            ip=ip,
            user_agent=user_agent,
            ciudad=geo['ciudad'],
            estado=geo['estado'],
            pais=geo['pais']
        )

    return render(request, 'Nexwork/trabajo_detalle.html', {
        'trabajo': trabajo,
        'img_profile': img_profile,
        'detalle': getattr(trabajo, 'detalle', None),
        'ya_postulado': ya_postulado,
    })

def mis_ofertas_view(request):
    return render(request, 'Nexwork/mis_ofertas.html') 

@login_required
def mis_ofertas_api(request):
    trabajos = Trabajo.objects.select_related('autor').filter(autor=request.user, activo=True)

    q = request.GET.get('q', '').strip()
    ubicacion = request.GET.get('ubicacion', '')
    modalidad = request.GET.get('modalidad', '')

    if q:
        trabajos = trabajos.filter(models.Q(titulo__icontains=q) | models.Q(descripcion__icontains=q))
    if ubicacion:
        trabajos = trabajos.filter(ubicacion__iexact=ubicacion)
    if modalidad:
        trabajos = trabajos.filter(modalidad__iexact=modalidad)

    trabajos = trabajos.order_by('-fecha_publicacion')

    data = []
    for t in trabajos:
        total_postulaciones = Postulacion.objects.filter(trabajo=t).count()

        if t.autor.img_profile:
            img_profile = f"data:image/jpeg;base64,{base64.b64encode(t.autor.img_profile).decode()}"
        else:
            img_profile = static('images/Nexwork/default-profile.png')

        data.append({
            'id': t.id,
            'titulo': t.titulo,
            'descripcion': t.descripcion[:100] + '...' if len(t.descripcion) > 100 else t.descripcion,
            'ubicacion': t.ubicacion,
            'modalidad': t.modalidad.title(),
            'fecha': t.fecha_publicacion.strftime('%d %b %Y'),
            'autor': f"{t.autor.nombre} {t.autor.apellidos}",
            'img_profile': img_profile,
            'postulaciones': total_postulaciones,
        })

    return JsonResponse({'ofertas': data})

@login_required
def postulaciones_usuarios_api(request, trabajo_id):
    search = request.GET.get('search', '').strip().lower()
    orden = request.GET.get('orden', 'recientes')

    postulaciones = Postulacion.objects.select_related('usuario').filter(trabajo_id=trabajo_id)

    if search:
        postulaciones = postulaciones.filter(
            models.Q(usuario__nombre__icontains=search) |
            models.Q(usuario__apellidos__icontains=search) |
            models.Q(usuario__correo__icontains=search) |
            models.Q(usuario__telefono__icontains=search)
        )

    if orden == 'antiguos':
        postulaciones = postulaciones.order_by('fecha_postulacion')
    else:
        postulaciones = postulaciones.order_by('-fecha_postulacion')

    data = []
    for p in postulaciones:
        u = p.usuario
        img = f"data:image/jpeg;base64,{base64.b64encode(u.img_profile).decode()}" if u.img_profile else '/static/images/Nexwork/default-profile.png'

        experiencias = [
            {
                'puesto': exp.puesto,
                'empresa': exp.empresa,
                'inicio': exp.fecha_inicio.strftime('%b %Y'),
                'fin': exp.fecha_fin.strftime('%b %Y') if exp.fecha_fin else 'Actual',
                'tecnologias': exp.tecnologias
            }
            for exp in u.experiencias.all()[:2]
        ]

        educacion = [
            {
                'titulo': e.titulo,
                'institucion': e.institucion,
                'inicio': e.fecha_inicio.strftime('%Y'),
                'fin': e.fecha_fin.strftime('%Y') if e.fecha_fin else 'Actual',
                'areas': e.areas_estudio
            }
            for e in u.educacion.all()[:2]
        ]

        data.append({
            'id': u.id,
            'nombre': f"{u.nombre} {u.apellidos}",
            'telefono': u.telefono,
            'correo': u.correo,
            'ocupacion': u.ocupacion,
            'img_profile': img,
            'experiencia': experiencias,
            'educacion': educacion,
            'mensaje': p.mensaje,
            'fecha_postulacion': p.fecha_postulacion.strftime('%d %b %Y'),
        })

    return JsonResponse({'usuarios': data})

@login_required
def postulaciones_recibidas_view(request, id):
    trabajo = get_object_or_404(Trabajo.objects.select_related('autor'), pk=id, autor=request.user)

    if trabajo.autor.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(trabajo.autor.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    return render(request, 'Nexwork/postulaciones_recibidas.html', {
        'trabajo_id': id,
        'trabajo': trabajo,
        'img_profile': img_profile
    })

@login_required
def estadisticas_trabajo_view(request, id):
    trabajo = get_object_or_404(Trabajo.objects.select_related('autor'), pk=id, activo=True)

    if trabajo.autor.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(trabajo.autor.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    total_vistas = trabajo.vistas.count()
    total_postulaciones = trabajo.postulaciones.count()
    conversion_rate = round((total_postulaciones / total_vistas) * 100, 2) if total_vistas > 0 else 0

    return render(request, 'Nexwork/estadisticas_trabajo.html', {
        'trabajo': trabajo,
        'img_profile': img_profile,
        'total_vistas': total_vistas,
        'total_postulaciones': total_postulaciones,
        'conversion_rate': conversion_rate,
    })

@login_required
def vistas_por_pais_api(request, id):
    trabajo = get_object_or_404(Trabajo, pk=id, activo=True)

    # Filtros GET
    fecha_inicio = request.GET.get('fecha_inicio')
    paises_param = request.GET.get('paises')  # lista de países separados por comas
    pais_filtro = request.GET.get('pais')     # filtro por un solo país
    estado_filtro = request.GET.get('estado')
    ciudad_filtro = request.GET.get('ciudad')

    vistas = trabajo.vistas.all()

    # Filtro por fecha
    if fecha_inicio:
        fecha_obj = parse_date(fecha_inicio)
        if fecha_obj:
            vistas = vistas.filter(fecha__date__gte=fecha_obj)

    # Filtro por varios países (coma separados)
    if paises_param:
        paises_lista = [p.strip() for p in paises_param.split(',')]
        vistas = vistas.filter(pais__in=paises_lista)

    # Filtros individuales
    if pais_filtro:
        vistas = vistas.filter(pais__iexact=pais_filtro)
    if estado_filtro:
        vistas = vistas.filter(estado__iexact=estado_filtro)
    if ciudad_filtro:
        vistas = vistas.filter(ciudad__iexact=ciudad_filtro)

    # Agrupaciones
    def agrupar_por(campo):
        return list(
            vistas.values(campo)
            .annotate(total=Count('id'))
            .order_by('-total')
        )

    data = {
        'paises': agrupar_por('pais'),
        'estados': agrupar_por('estado'),
        'ciudades': agrupar_por('ciudad'),
    }
    return JsonResponse(data)