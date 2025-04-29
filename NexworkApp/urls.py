from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from NexworkApp import views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    path('login', views.login_view, name='login'),
    path('login_auth', views.login_auth, name='login_auth'),

    path('api/publicaciones/', views.publicaciones_publicas, name='publicaciones_publicas'),
    path('api/publicaciones/nueva/', views.nueva_publicacion, name='nueva_publicacion'),
    path('api/publicaciones/<int:id>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('api/publicaciones/<int:id>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('api/likes/<int:id>/', views.toggle_like_publicacion, name='toggle_like_publicacion'),
    path('api/comentarios/<int:publicacion_id>/', views.obtener_comentarios, name='obtener_comentarios'),
    path('api/comentarios/nuevo/<int:publicacion_id>/', views.nuevo_comentario, name='nuevo_comentario'),
    path('api/comentarios/editar/<int:id>/', views.editar_comentario, name='editar_comentario'),
    path('api/comentarios/eliminar/<int:id>/', views.eliminar_comentario, name='eliminar_comentario'),



    #PROFILE
    path('profile/view/<int:id>/', views.profile_view, name='profile'),
    path('api/usuario/<int:id>/actualizar_img/', views.actualizar_img_profile, name='actualizar_img_profile'),
    path('api/usuario/<int:id>/actualizar_banner/', views.actualizar_banner_profile, name='actualizar_banner_profile'),
    






]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
