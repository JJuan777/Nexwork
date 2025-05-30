from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError("El nombre de usuario es obligatorio")
        extra_fields.setdefault('is_active', True)
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(usuario, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    correo = models.EmailField(unique=True)
    usuario = models.CharField(max_length=50, unique=True)

    ocupacion = models.CharField(max_length=100, blank=True, null=True)  # <--- nuevo campo

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    reset_password = models.BooleanField(default=False)

    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, blank=True)

    img_profile = models.BinaryField(blank=True, null=True)  
    banner_profile = models.BinaryField(blank=True, null=True) 

    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['correo', 'nombre', 'apellidos']

    def __str__(self):
        return self.usuario
    
class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
class Publicacion(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publicaciones')
    descripcion = models.TextField(verbose_name='Descripción')
    imagen = models.BinaryField(blank=True, null=True)
    archivo = models.BinaryField(blank=True, null=True)
    nombre_archivo = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    es_publico = models.BooleanField(default=True)

    def __str__(self):
        return f"Publicación de {self.autor.usuario} - {self.fecha_creacion.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-fecha_creacion']

class PublicacionCompartida(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publicaciones_compartidas')
    publicacion_original = models.ForeignKey('Publicacion', on_delete=models.CASCADE, related_name='compartidas')
    fecha_compartida = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)  # Comentario del usuario al compartir
    es_publico = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.usuario} compartió publicación {self.publicacion_original.id}"

class SolicitudAmistad(models.Model):
    de_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_enviadas'
    )
    para_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_recibidas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('aceptada', 'Aceptada'),
            ('rechazada', 'Rechazada'),
            ('cancelada', 'Cancelada'),
        ],
        default='pendiente'
    )

    class Meta:
        unique_together = ('de_usuario', 'para_usuario')

    def __str__(self):
        return f"{self.de_usuario} → {self.para_usuario} ({self.estado})"

class Amistad(models.Model):
    usuario1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='amistades_usuario1'
    )
    usuario2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='amistades_usuario2'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario1', 'usuario2')

    def __str__(self):
        return f"{self.usuario1} & {self.usuario2}"

class Like(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='likes'
    )
    publicacion = models.ForeignKey(
        'Publicacion',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'publicacion')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f"{self.usuario.usuario} dio like a Publicación {self.publicacion.id}"

class Comentario(models.Model):
    publicacion = models.ForeignKey(
        'Publicacion', 
        on_delete=models.CASCADE, 
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    contenido = models.TextField(verbose_name='Comentario')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.usuario} comentó en Publicación {self.publicacion.id}"

    class Meta:
        ordering = ['-fecha_creacion']

class Trabajo(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trabajos_publicados')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    modalidad = models.CharField(max_length=50, choices=[('remoto', 'Remoto'), ('presencial', 'Presencial'), ('híbrido', 'Híbrido')])
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor.usuario}"
    
class TrabajoDetalle(models.Model):
    trabajo = models.OneToOneField('Trabajo', on_delete=models.CASCADE, related_name='detalle')

    # Campos existentes
    area = models.CharField(max_length=100, blank=True, null=True)
    nivel_experiencia = models.CharField(max_length=100, blank=True, null=True)
    habilidades_tecnicas = models.TextField(blank=True, null=True)
    habilidades_blandas = models.TextField(blank=True, null=True)
    tipo_contrato = models.CharField(max_length=100, choices=[
        ('tiempo_completo', 'Tiempo completo'),
        ('medio_tiempo', 'Medio tiempo'),
        ('freelance', 'Freelance'),
        ('temporal', 'Temporal'),
        ('prácticas', 'Prácticas profesionales'),
    ], blank=True, null=True)
    salario_estimado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duracion_meses = models.PositiveIntegerField(blank=True, null=True)
    idiomas = models.CharField(max_length=255, blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    horario_laboral = models.CharField(max_length=100, blank=True, null=True)  # Ej: L-V 9:00 a 18:00
    beneficios = models.TextField(blank=True, null=True)  # Ej: Seguro médico, vales de despensa
    disponibilidad_viajar = models.BooleanField(default=False)
    disponibilidad_cambio_residencia = models.BooleanField(default=False)
    numero_vacantes = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Detalle del trabajo: {self.trabajo.titulo}"
    
class VistaTrabajo(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='vistas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.trabajo} visto por {self.usuario or self.ip}"
    
class Postulacion(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='postulaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='postulaciones')
    mensaje = models.TextField(blank=True)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trabajo', 'usuario')  # Un usuario no puede postularse dos veces al mismo trabajo

    def __str__(self):
        return f"{self.usuario.usuario} → {self.trabajo.titulo}"

class ExperienciaLaboral(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='experiencias')
    puesto = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)  # Opcional
    tecnologias = models.CharField(max_length=255, blank=True)  # Ej: Python, Django, APIs

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.puesto} en {self.empresa}"

class Educacion(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='educacion')
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    areas_estudio = models.CharField(max_length=255, blank=True)  # Ej: Bases de Datos, Redes, Programación

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"

class VisitaPerfil(models.Model):
    perfil = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='visitas_recibidas'
    )
    visitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='visitas_realizadas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Visita de perfil'
        verbose_name_plural = 'Visitas de perfiles'
        unique_together = ('perfil', 'visitante', 'fecha')  # opcional para evitar duplicados extremos

    def __str__(self):
        return f"{self.visitante} visitó a {self.perfil} el {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('amistad', 'Amistad'),
        ('postulacion', 'Postulación'),
        ('comentario', 'Comentario'),
        ('like', 'Like'),
        ('compartido', 'Publicación compartida'),
        ('sistema', 'Sistema'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    url = models.CharField(max_length=255, blank=True, help_text="Enlace donde redirige la notificación")
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.usuario} → {self.tipo} | {'leído' if self.leido else 'nuevo'}"

    class Meta:
        ordering = ['-fecha']

class Conversacion(models.Model):
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversaciones')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversación {self.id} - {', '.join([p.usuario for p in self.participantes.all()])}"


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    texto = models.TextField(blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)  # Para imágenes
    archivo = models.FileField(upload_to='mensajes_archivos/', blank=True, null=True)  # Para archivos
    enviado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.remitente.usuario} en Conversación {self.conversacion.id}"
    

class Historia(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historias')
    imagen = models.BinaryField(null=True, blank=True)  # VARBINARY para imagen
    texto = models.CharField(max_length=255, blank=True)  # opcional, como subtítulo o descripción
    creado_en = models.DateTimeField(auto_now_add=True)
    expirado = models.BooleanField(default=False)  # si ya pasó su tiempo de vida

    def __str__(self):
        return f"Historia de {self.autor.usuario} - {self.creado_en.strftime('%Y-%m-%d %H:%M')}"