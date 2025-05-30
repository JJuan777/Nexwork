from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse, HttpResponseForbidden
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
from datetime import date
from .models import Usuario
from .models import Publicacion, Amistad, Like, Comentario, PublicacionCompartida, SolicitudAmistad
from .models import ExperienciaLaboral, Educacion, Rol
from .models import Conversacion, Mensaje, Historia
from django.utils.dateparse import parse_date
from .models import Trabajo, Postulacion
import json
from django.db.models import Q
import base64, requests
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count
from .models import VistaTrabajo,VisitaPerfil
from .models import Notificacion
from django.utils.html import escape
from base64 import b64encode
from django.utils.timesince import timesince

# Create your views here.
@login_required
def home_view(request):
    usuario = request.user

    trabajos = Trabajo.objects.filter(activo=True).select_related('autor').order_by('-fecha_publicacion')[:2]

    visitas_perfil = VisitaPerfil.objects.filter(perfil=usuario).count()
    publicaciones = Publicacion.objects.filter(autor=usuario).count()
    amistades = Amistad.objects.filter(
        Q(usuario1=usuario) | Q(usuario2=usuario)
    ).count()

    return render(request, 'Nexwork/index.html', {
        'trabajos_recientes': trabajos,
        'visitas_perfil': visitas_perfil,
        'publicaciones_count': publicaciones,
        'amistades_count': amistades,
    })

def login_view(request):
    return render(request, 'Nexwork/auth/login.html') 

def registro_view(request):
    roles = Rol.objects.all()
    return render(request, 'Nexwork/auth/registro.html', {
        'roles': roles
    })

@csrf_exempt
def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        correo = request.POST.get('correo')
        usuario = request.POST.get('usuario')
        ocupacion = request.POST.get('ocupacion')
        telefono = request.POST.get('telefono', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        rol_id = request.POST.get('rol_id')
        img_profile = request.FILES.get('img_profile')
        banner_profile = request.FILES.get('banner_profile')

        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Las contraseñas no coinciden.'})

        if Usuario.objects.filter(usuario=usuario).exists():
            return JsonResponse({'success': False, 'error': 'El usuario ya está registrado.'})

        if Usuario.objects.filter(correo=correo).exists():
            return JsonResponse({'success': False, 'error': 'El correo ya está en uso.'})

        try:
            rol = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Rol seleccionado no válido.'})

        user = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            usuario=usuario,
            ocupacion=ocupacion,
            telefono=telefono,
            rol=rol
        )
        if img_profile:
            user.img_profile = img_profile.read()
        if banner_profile:
            user.banner_profile = banner_profile.read()

        user.set_password(password1)
        user.save()

        login(request, user)

        return JsonResponse({'success': True, 'redirect': '/profile-nexwork'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

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

@login_required
def profile_view(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    actual = request.user

    # Registrar visita (solo si es otro usuario y aún no visitó hoy)
    if actual != usuario:
        ya_visito_hoy = VisitaPerfil.objects.filter(
            perfil=usuario,
            visitante=actual,
            fecha__date=date.today()
        ).exists()

        if not ya_visito_hoy:
            VisitaPerfil.objects.create(
                perfil=usuario,
                visitante=actual,
                ip=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

    # Imagen de perfil
    if usuario.img_profile:
        img_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.img_profile).decode()}"
    else:
        img_profile = static('images/Nexwork/default-profile.png')

    # Banner
    if usuario.banner_profile:
        banner_profile = f"data:image/jpeg;base64,{base64.b64encode(usuario.banner_profile).decode()}"
    else:
        banner_profile = static('images/Nexwork/default-banner.jpg')

    todas_experiencias = usuario.experiencias.order_by('-fecha_inicio')
    experiencias = todas_experiencias[:2]
    hay_mas_experiencias = todas_experiencias.count() > 2

    for exp in experiencias:
        exp.tecnologias_lista = [tag.strip() for tag in exp.tecnologias.split(',')] if exp.tecnologias else []

    educaciones = usuario.educacion.all()[:2]
    hay_mas_educacion = usuario.educacion.count() > 2

    for edu in educaciones:
        edu.areas_estudio_lista = [tag.strip() for tag in edu.areas_estudio.split(',')] if edu.areas_estudio else []

    ya_son_amigos = False
    solicitud_pendiente = False
    contactos = []

    if actual.is_authenticated:
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

        amistades = Amistad.objects.filter(Q(usuario1=usuario) | Q(usuario2=usuario))[:5]
        contactos = [a.usuario2 if a.usuario1 == usuario else a.usuario1 for a in amistades]

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
    solo_postulados = request.GET.get('solo_postulados') == 'on'

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

    # Mover aquí: necesario antes de usarlo
    usuario = request.user
    postulaciones = set(
        Postulacion.objects.filter(usuario=usuario).values_list('trabajo_id', flat=True)
    )

    # Filtro por solo postulados
    if solo_postulados:
        trabajos = trabajos.filter(id__in=postulaciones)

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

@login_required
def completa_perfil_view(request):
    return render(request, 'Nexwork/completa_perfil.html') 

def solicitudes_amistad_view(request):
    return render(request, 'Nexwork/solicitudes_amistad.html') 

@login_required
def solicitudes_api(request):
    solicitudes = SolicitudAmistad.objects.select_related('de_usuario').filter(
        para_usuario=request.user,
        estado='pendiente'
    )

    data = []
    for s in solicitudes:
        if s.de_usuario.img_profile:
            img_profile = f"data:image/jpeg;base64,{base64.b64encode(s.de_usuario.img_profile).decode()}"
        else:
            img_profile = '/static/images/Nexwork/default-profile.png'

        data.append({
            'id': s.id,
            'nombre': f"{s.de_usuario.nombre} {s.de_usuario.apellidos}",
            'usuario_id': s.de_usuario.id,
            'img_profile': img_profile,
            'fecha': s.fecha_creacion.strftime('%d %b %Y'),
        })

    return JsonResponse({'solicitudes': data})

@require_POST
@login_required
def procesar_solicitud_view(request, id):
    accion = request.POST.get('accion')

    try:
        solicitud = SolicitudAmistad.objects.get(id=id, para_usuario=request.user, estado='pendiente')

        if accion == 'aceptar':
            Amistad.objects.create(usuario1=solicitud.de_usuario, usuario2=solicitud.para_usuario)
            solicitud.estado = 'aceptada'
            solicitud.save()
            return JsonResponse({'success': True, 'mensaje': 'Solicitud aceptada.'})

        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            solicitud.save()
            return JsonResponse({'success': True, 'mensaje': 'Solicitud rechazada.'})

        else:
            return JsonResponse({'success': False, 'error': 'Acción no válida.'}, status=400)

    except SolicitudAmistad.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Solicitud no encontrada.'}, status=404)
    
@login_required
def contador_solicitudes_api(request):
    count = SolicitudAmistad.objects.filter(
        para_usuario=request.user,
        estado='pendiente'
    ).count()
    return JsonResponse({'count': count})

@login_required
def notificaciones_api(request):
    offset = int(request.GET.get('offset', 0))
    limite = 10

    notifs_qs = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')
    notifs = notifs_qs[offset:offset+limite]

    data = []
    for n in notifs:
        data.append({
            'id': n.id,
            'mensaje': n.mensaje,
            'url': n.url,
            'fecha': n.fecha.strftime('%d %b, %H:%M'),
            'leido': n.leido
        })

    total = notifs_qs.count()
    no_leidas = notifs_qs.filter(leido=False).count()
    return JsonResponse({
        'notificaciones': data,
        'no_leidas': no_leidas,
        'hay_mas': offset + limite < total
    })

@require_POST
@login_required
def marcar_notificacion_leida(request):
    notif_id = request.POST.get('id')
    try:
        noti = Notificacion.objects.get(id=notif_id, usuario=request.user)
        noti.leido = True
        noti.save()
        return JsonResponse({'success': True})
    except Notificacion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No encontrada'}, status=404)
    
@require_POST
@login_required
def eliminar_notificacion(request):
    notif_id = request.POST.get('id')
    try:
        noti = Notificacion.objects.get(id=notif_id, usuario=request.user)
        noti.delete()
        return JsonResponse({'success': True})
    except Notificacion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No encontrada'}, status=404)

@login_required
def settings_usuario_view(request):
    return render(request, 'Nexwork/settings_usuario.html') 

@login_required
def api_get_user_settings(request):
    usuario = request.user
    data = {
        "nombre": usuario.nombre,
        "apellidos": usuario.apellidos,
        "correo": usuario.correo,
        "usuario": usuario.usuario,
        "ocupacion": usuario.ocupacion if usuario.ocupacion else "",
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def api_update_user_settings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        usuario = request.user

        # Actualizar los datos del usuario
        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.apellidos = data.get("apellidos", usuario.apellidos)
        usuario.correo = data.get("correo", usuario.correo)
        usuario.usuario = data.get("usuario", usuario.usuario)
        usuario.ocupacion = data.get("ocupacion", usuario.ocupacion)
        usuario.save()

        return JsonResponse({"success": True, "message": "Cambios guardados correctamente."})
    
    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

@login_required
@csrf_exempt
def api_update_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nueva_contrasena = data.get("nueva_contrasena")
        confirmar_contrasena = data.get("confirmar_contrasena")

        if nueva_contrasena != confirmar_contrasena:
            return JsonResponse({"success": False, "message": "Las contraseñas no coinciden."})

        if len(nueva_contrasena) < 8:
            return JsonResponse({"success": False, "message": "La contraseña debe tener al menos 8 caracteres."})

        usuario = request.user
        usuario.set_password(nueva_contrasena)
        usuario.save()

        return JsonResponse({"success": True, "message": "Contraseña actualizada correctamente."})
    
    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

@login_required
def eliminar_contacto(request, usuario_id):
    if request.method == 'POST':
        usuario_actual = request.user

        # Eliminar amistad
        amistad = Amistad.objects.filter(
            Q(usuario1=usuario_actual, usuario2_id=usuario_id) |
            Q(usuario2=usuario_actual, usuario1_id=usuario_id)
        ).first()
        if amistad:
            amistad.delete()

        # Eliminar cualquier solicitud entre ambos (enviada o recibida)
        SolicitudAmistad.objects.filter(
            Q(de_usuario=usuario_actual, para_usuario_id=usuario_id) |
            Q(para_usuario=usuario_actual, de_usuario_id=usuario_id)
        ).delete()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def mensaje_view(request):
    return render(request, 'Nexwork/mensaje.html') 

@login_required
def listar_conversaciones_api(request):
    usuario = request.user
    conversaciones = Conversacion.objects.filter(participantes=usuario, mensajes__isnull=False).distinct()

    data = []
    for conversacion in conversaciones:
        ultimo_mensaje = conversacion.mensajes.last()
        if ultimo_mensaje:
            for participante in conversacion.participantes.all():
                if participante != usuario:
                    # Verificar si el usuario tiene imagen de perfil
                    if participante.img_profile:
                        img_data = base64.b64encode(participante.img_profile).decode('utf-8')
                        img_url = f"data:image/png;base64,{img_data}"
                    else:
                        img_url = static('images/Nexwork/default-profile.png')

                    data.append({
                        'id': conversacion.id,
                        'participante_nombre': participante.usuario,
                        'img_url': img_url,
                        'ultimo_mensaje': escape(ultimo_mensaje.texto),
                        'fecha_ultimo_mensaje': ultimo_mensaje.enviado_en,
                    })

    return JsonResponse({'conversaciones': data})

@login_required
def listar_amistades_api(request):
    usuario = request.user
    amistades = Amistad.objects.filter(usuario1=usuario) | Amistad.objects.filter(usuario2=usuario)
    amigos = []

    for amistad in amistades:
        amigo = amistad.usuario2 if amistad.usuario1 == usuario else amistad.usuario1
        
        # Convertir la imagen en base64 si existe
        if amigo.img_profile:
            img_base64 = f"data:image/jpeg;base64,{base64.b64encode(amigo.img_profile).decode('utf-8')}"
        else:
            img_base64 = ''

        amigos.append({
            'id': amigo.id,
            'usuario': amigo.usuario,
            'nombre': amigo.nombre,
            'img_profile': img_base64
        })

    return JsonResponse({'amigos': amigos})

@login_required
def cargar_mensajes_api(request, conversacion_id=None):
    usuario = request.user

    # Si el ID de conversación es nulo o no existe, crear la conversación
    if conversacion_id is None or not Conversacion.objects.filter(id=conversacion_id, participantes=usuario).exists():
        # Crear una nueva conversación entre el usuario autenticado y otro participante (requiere definir el otro participante)
        otro_usuario_id = request.GET.get("otro_usuario_id")
        if otro_usuario_id:
            otro_usuario = get_object_or_404(Usuario, id=otro_usuario_id)
            conversacion, creada = Conversacion.objects.get_or_create()
            conversacion.participantes.add(usuario, otro_usuario)
            conversacion.save()
        else:
            return JsonResponse({'error': 'Debe especificar el otro usuario para crear la conversación.'}, status=400)
    else:
        conversacion = get_object_or_404(Conversacion, id=conversacion_id, participantes=usuario)

    # Obtener mensajes de la conversación
    mensajes = conversacion.mensajes.order_by('enviado_en')

    data = [
        {
            'id': mensaje.id,
            'texto': mensaje.texto,
            'es_mio': mensaje.remitente == request.user
        }
        for mensaje in mensajes
    ]

    return JsonResponse({'mensajes': data, 'conversacion_id': conversacion.id})

@login_required
def enviar_mensaje_api(request, conversacion_id):
    if request.method == 'POST':
        conversacion = get_object_or_404(Conversacion, id=conversacion_id, participantes=request.user)
        data = json.loads(request.body)
        texto = data.get('texto')

        if texto:
            mensaje = Mensaje.objects.create(
                conversacion=conversacion,
                remitente=request.user,
                texto=texto
            )

            return JsonResponse({
                'success': True,
                'mensaje': {
                    'id': mensaje.id,
                    'texto': mensaje.texto,
                    'es_mio': True
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'El mensaje no puede estar vacío.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

@login_required
def filtrar_amigos(request):
    query = request.GET.get('q', '')
    usuario = request.user

    amigos = Usuario.objects.filter(
        Q(nombre__icontains=query) | Q(apellidos__icontains=query)
    ).exclude(id=usuario.id)[:5]  # Limitar a 5 resultados

    amigos_data = []

    for amigo in amigos:
        # Buscar la conversación entre el usuario y el amigo
        conversacion = Conversacion.objects.filter(participantes=usuario).filter(participantes=amigo).first()
        
        # Obtener la imagen del amigo
        if amigo.img_profile:
            img_data = base64.b64encode(amigo.img_profile).decode('utf-8')
            img_url = f"data:image/png;base64,{img_data}"
        else:
            img_url = static('images/Nexwork/default-profile.png')
        
        amigos_data.append({
            'id_conversacion': conversacion.id if conversacion else None,
            'nombre': f"{amigo.nombre} {amigo.apellidos}",
            'id_sesion': usuario.id,
            'id_amigo': amigo.id,  # ID del amigo
            'img_url': img_url  # URL de la imagen
        })

    return JsonResponse({'amigos': amigos_data})

@login_required
def crear_conversacion(request):
    usuario = request.user
    otro_usuario_id = request.GET.get('otro_usuario_id')

    if not otro_usuario_id:
        return JsonResponse({'error': 'No se proporcionó el ID del otro usuario.'}, status=400)

    otro_usuario = get_object_or_404(Usuario, id=otro_usuario_id)

    # Verificar si ya existe una conversación entre los dos
    conversacion = Conversacion.objects.filter(
        participantes=usuario
    ).filter(participantes=otro_usuario).distinct().first()

    # Crear la conversación si no existe
    if not conversacion:
        conversacion = Conversacion.objects.create()
        conversacion.participantes.add(usuario, otro_usuario)
        conversacion.save()

    return JsonResponse({'id_conversacion': conversacion.id})

@login_required
def historias_amistades_view(request):
    usuario = request.user

    # Obtener IDs de amigos (bidireccional)
    amigos_ids_1 = Amistad.objects.filter(usuario1=usuario).values_list('usuario2', flat=True)
    amigos_ids_2 = Amistad.objects.filter(usuario2=usuario).values_list('usuario1', flat=True)
    amigos_ids = set(amigos_ids_1).union(set(amigos_ids_2))

    # Agregar el propio usuario
    amigos_ids.add(usuario.id)

    # Filtrar historias no expiradas
    historias = Historia.objects.filter(
        autor__id__in=amigos_ids,
        expirado=False
    ).order_by('-creado_en')[:30]

    historias_data = []
    for h in historias:
        imagen_base64 = None
        if h.imagen:
            try:
                imagen_base64 = f"data:image/jpeg;base64,{b64encode(h.imagen).decode()}"
            except Exception as e:
                print(f"⚠️ Error al codificar imagen de la historia {h.id}: {e}")

        historias_data.append({
        'id': h.id,
        'nombre': f"{h.autor.nombre} {h.autor.apellidos}",
        'imagen': imagen_base64,
        'texto': h.texto or "",
        'es_mia': h.autor_id == usuario.id,
        'autor': f"{h.autor.nombre} {h.autor.apellidos}",
        'hora': timesince(h.creado_en) + " atrás"
    })

    return JsonResponse({'historias': historias_data})

@csrf_exempt
@require_POST
@login_required
def publicar_historia_view(request):
    usuario = request.user
    imagen = request.FILES.get('imagen')
    texto = request.POST.get('texto', '').strip()

    if not imagen:
        return JsonResponse({'error': 'Imagen requerida'}, status=400)

    historia = Historia.objects.create(
        autor=usuario,
        imagen=imagen.read(),  # guardamos como binario
        texto=texto
    )
    return JsonResponse({'success': True, 'historia_id': historia.id})

@require_http_methods(["DELETE"])
@login_required
def eliminar_historia_view(request, id):
    try:
        historia = Historia.objects.get(id=id, autor=request.user)
        historia.delete()
        return JsonResponse({'success': True})
    except Historia.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para eliminar esta historia.")