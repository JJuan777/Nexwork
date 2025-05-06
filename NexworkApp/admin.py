from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Rol, Publicacion, SolicitudAmistad, Amistad, Like, Comentario, PublicacionCompartida, ExperienciaLaboral,Educacion
from .models import Trabajo, Postulacion, TrabajoDetalle, VistaTrabajo


class UsuarioAdmin(BaseUserAdmin):
    list_display = ('id', 'usuario', 'nombre', 'apellidos', 'correo', 'ocupacion', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'reset_password')
    search_fields = ('usuario', 'correo', 'nombre', 'apellidos', 'ocupacion')
    ordering = ('id',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('usuario', 'password')}),
        ('Información personal', {
            'fields': (
                'nombre', 'apellidos', 'correo', 'telefono', 'ocupacion', 'rol',
            )
        }),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'reset_password'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'usuario', 'nombre', 'apellidos', 'correo', 'telefono', 'ocupacion', 'rol',
                'password1', 'password2',
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )

class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('id',)


class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'descripcion_corta', 'fecha_creacion', 'es_publico')
    list_filter = ('es_publico', 'fecha_creacion')
    search_fields = ('descripcion', 'autor__usuario', 'autor__nombre')
    ordering = ('-fecha_creacion',)

    def descripcion_corta(self, obj):
        return (obj.descripcion[:50] + '...') if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'


class SolicitudAmistadAdmin(admin.ModelAdmin):
    list_display = ('id', 'de_usuario', 'para_usuario', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('de_usuario__usuario', 'para_usuario__usuario')
    ordering = ('-fecha_creacion',)


class AmistadAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario1', 'usuario2', 'fecha_creacion')
    search_fields = ('usuario1__usuario', 'usuario2__usuario')
    ordering = ('-fecha_creacion',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'publicacion', 'fecha_creacion')
    search_fields = ('usuario__usuario', 'publicacion__descripcion')
    list_filter = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'publicacion', 'autor', 'contenido_corto', 'fecha_creacion')
    search_fields = ('contenido', 'autor__usuario')
    ordering = ('-fecha_creacion',)

    def contenido_corto(self, obj):
        return (obj.contenido[:50] + '...') if len(obj.contenido) > 50 else obj.contenido
    
class PublicacionCompartidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'publicacion_original', 'comentario_corto', 'fecha_compartida', 'es_publico')
    list_filter = ('es_publico', 'fecha_compartida')
    search_fields = ('usuario__usuario', 'publicacion_original__descripcion')

    def comentario_corto(self, obj):
        return (obj.comentario[:50] + '...') if obj.comentario and len(obj.comentario) > 50 else obj.comentario
    comentario_corto.short_description = 'Comentario'

class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'ubicacion', 'modalidad', 'activo', 'fecha_publicacion')
    list_filter = ('modalidad', 'activo', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion', 'autor__usuario')
    ordering = ('-fecha_publicacion',)

class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'trabajo', 'usuario', 'fecha_postulacion')
    search_fields = ('trabajo__titulo', 'usuario__usuario')
    list_filter = ('fecha_postulacion',)
    ordering = ('-fecha_postulacion',)

class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'puesto', 'empresa', 'fecha_inicio', 'fecha_fin')
    search_fields = ('usuario__usuario', 'empresa', 'puesto')
    list_filter = ('empresa', 'fecha_inicio', 'fecha_fin')
    ordering = ('-fecha_inicio',)

class EducacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'titulo', 'institucion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('usuario__usuario', 'titulo', 'institucion')
    list_filter = ('institucion', 'fecha_inicio', 'fecha_fin')
    ordering = ('-fecha_inicio',)
    
class TrabajoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'trabajo',
        'area',
        'nivel_experiencia',
        'tipo_contrato',
        'salario_estimado',
        'fecha_limite',
        'numero_vacantes'
    )
    search_fields = (
        'trabajo__titulo',
        'area',
        'nivel_experiencia',
        'habilidades_tecnicas',
        'habilidades_blandas'
    )
    list_filter = (
        'area',
        'nivel_experiencia',
        'tipo_contrato',
        'fecha_limite',
        'disponibilidad_viajar',
        'disponibilidad_cambio_residencia'
    )
    ordering = ('-fecha_limite',)

class VistaTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'trabajo', 'usuario', 'ip', 'ciudad', 'estado', 'pais', 'fecha'
    )
    search_fields = (
        'trabajo__titulo', 'usuario__usuario', 'ip', 'user_agent', 'ciudad', 'estado', 'pais'
    )
    list_filter = ('trabajo', 'fecha', 'pais', 'estado')
    ordering = ('-fecha',)



# Registro de modelos
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(PublicacionCompartida, PublicacionCompartidaAdmin)
admin.site.register(ExperienciaLaboral, ExperienciaLaboralAdmin)
admin.site.register(TrabajoDetalle, TrabajoDetalleAdmin)
admin.site.register(VistaTrabajo, VistaTrabajoAdmin)
admin.site.register(Educacion, EducacionAdmin)
admin.site.register(Trabajo, TrabajoAdmin)
admin.site.register(Postulacion, PostulacionAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(SolicitudAmistad, SolicitudAmistadAdmin)
admin.site.register(Amistad, AmistadAdmin)
