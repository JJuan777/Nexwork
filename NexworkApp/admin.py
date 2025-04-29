from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Rol, Publicacion, SolicitudAmistad, Amistad


class UsuarioAdmin(BaseUserAdmin):
    list_display = ('id', 'usuario', 'nombre', 'apellidos', 'correo', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'reset_password')
    search_fields = ('usuario', 'correo', 'nombre', 'apellidos')
    ordering = ('id',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('usuario', 'password')}),
        ('Información personal', {
            'fields': (
                'nombre', 'apellidos', 'correo', 'telefono', 'rol',
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
                'usuario', 'nombre', 'apellidos', 'correo', 'telefono', 'rol',
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


# Registro de modelos
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(SolicitudAmistad, SolicitudAmistadAdmin)
admin.site.register(Amistad, AmistadAdmin)
