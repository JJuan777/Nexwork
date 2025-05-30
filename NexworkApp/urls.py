from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from NexworkApp import views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    #HISTORIAs
    path('api/historias/', views.historias_amistades_view, name='api_historias'),
    path('api/historias/publicar/', views.publicar_historia_view, name='publicar_historia'),
    path('api/historias/eliminar/<int:id>/', views.eliminar_historia_view, name='eliminar_historia'),


    path('login', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('api/registro/', views.registro_usuario, name='registro_usuario'),
    path('login_auth', views.login_auth, name='login_auth'),
    path('logout/', views.logout_view, name='logout'),

    path('api/publicaciones/', views.publicaciones_publicas, name='publicaciones_publicas'),
    path('api/publicaciones/nueva/', views.nueva_publicacion, name='nueva_publicacion'),
    path('api/publicaciones/<int:id>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('api/publicaciones/<int:id>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('api/publicaciones_compartidas/<int:id>/eliminar/', views.eliminar_publicacion_compartida, name='eliminar_publicacion_compartida'),
    path('api/likes/<int:id>/', views.toggle_like_publicacion, name='toggle_like_publicacion'),
    path('api/comentarios/<int:publicacion_id>/', views.obtener_comentarios, name='obtener_comentarios'),
    path('api/comentarios/nuevo/<int:publicacion_id>/', views.nuevo_comentario, name='nuevo_comentario'),
    path('api/comentarios/editar/<int:id>/', views.editar_comentario, name='editar_comentario'),
    path('api/comentarios/eliminar/<int:id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('api/publicaciones/compartir/', views.compartir_publicacion, name='compartir_publicacion'),
    path('api/solicitudes/enviar/', views.enviar_solicitud_amistad, name='enviar_solicitud_amistad'),

    #PROFILE
    path('profile/view/<int:id>/', views.profile_view, name='profile'),
    path('api/usuario/<int:id>/actualizar_img/', views.actualizar_img_profile, name='actualizar_img_profile'),
    path('api/usuario/<int:id>/actualizar_banner/', views.actualizar_banner_profile, name='actualizar_banner_profile'),
    path('settings/', views.settings_usuario_view, name='settings_usuario_view'),
    path('api/user/settings/', views.api_get_user_settings, name='api_get_user_settings'),
    path('api/user/settings/update/', views.api_update_user_settings, name='api_update_user_settings'),
    path('api/user/settings/update-password/', views.api_update_password, name='api_update_password'),
    path('api/eliminar-contacto/<int:usuario_id>/', views.eliminar_contacto, name='eliminar_contacto'),

            #experiencias
    path('profile/<int:id>/experiencias/', views.experiencias_usuario, name='profile_experiencias'),
    path('api/usuario/<int:id>/experiencias/', views.api_experiencias_usuario, name='api_experiencias_usuario'),
    path('api/experiencia/<int:id>/actualizar/', views.actualizar_experiencia, name='actualizar_experiencia'),
    path('api/usuario/<int:id>/experiencias/nueva/', views.nueva_experiencia, name='nueva_experiencia'),
    path('api/experiencia/<int:id>/eliminar/', views.eliminar_experiencia, name='eliminar_experiencia'),
            #educacion
    path('profile/<int:id>/educacion/', views.educacion_usuario, name='educacion_usuario'),
    path('api/usuario/<int:id>/educacion/', views.api_educacion_usuario, name='api_educacion_usuario'),
    path('api/educacion/<int:id>/actualizar/', views.actualizar_educacion, name='actualizar_educacion'),
    path('api/educacion/<int:id>/eliminar/', views.eliminar_educacion, name='eliminar_educacion'),
    path('api/usuario/<int:id>/educacion/crear/', views.crear_educacion, name='crear_educacion'),
    
    #TRABAJOS
    path('newworks/', views.trabajos_view, name='trabajos'),
    path('api/trabajos/', views.trabajos_api, name='api_trabajos'),
    path('api/trabajos/<int:id>/postularse/', views.postularse_trabajo, name='postularse_trabajo'),
    path('newworks/view/<int:id>/', views.trabajo_detalle_view, name='trabajo_detalle'),
    path('ofertas/', views.mis_ofertas_view, name='mis_ofertas_view'),
    path('api/mis-ofertas/', views.mis_ofertas_api, name='api_mis_ofertas'),
    path('api/postulaciones/<int:trabajo_id>/usuarios/', views.postulaciones_usuarios_api, name='postulaciones_usuarios_api'),
    path('newworks/postulaciones/<int:id>/', views.postulaciones_recibidas_view, name='postulaciones_recibidas_view'),
    path('estadisticas/view/<int:id>/', views.estadisticas_trabajo_view, name='estadisticas_trabajo_view'),
    path('api/vistas-por-pais/<int:id>/', views.vistas_por_pais_api, name='vistas_por_pais_api'),

    path('profile-nexwork', views.completa_perfil_view, name='completa_perfil_view'),

    #Solicitudes de amistad
    path('solicitudes/', views.solicitudes_amistad_view, name='solicitudes'),
    path('api/solicitudes/', views.solicitudes_api, name='api_solicitudes'),
    path('api/solicitudes/<int:id>/procesar/', views.procesar_solicitud_view, name='procesar_solicitud'),
    path('api/contador-solicitudes/', views.contador_solicitudes_api, name='contador_solicitudes'),

    #Notificaciones
    path('api/notificaciones/', views.notificaciones_api, name='api_notificaciones'),
    path('api/notificaciones/marcar-leida/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('api/notificaciones/eliminar/', views.eliminar_notificacion, name='eliminar_notificacion'),

    path('mensajes/', views.mensaje_view, name='mensaje_view'),
    path('api/conversaciones/', views.listar_conversaciones_api, name='api_listar_conversaciones'),
    path('api/amistades/', views.listar_amistades_api, name='api_listar_amistades'),
    path('api/mensajes/<int:conversacion_id>/', views.cargar_mensajes_api, name='api_cargar_mensajes'),
    path('api/mensajes/<int:conversacion_id>/enviar/', views.enviar_mensaje_api, name='api_enviar_mensaje'),
    path('api/filtrar_amigos/', views.filtrar_amigos, name='filtrar_amigos'),
    path('api/crear_conversacion/', views.crear_conversacion, name='crear_conversacion'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
