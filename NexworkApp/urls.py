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
    path('api/publicaciones/<int:id>/eliminar_imagen/', views.eliminar_imagen_publicacion, name='eliminar_imagen_publicacion'),
    path('api/publicaciones/<int:id>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
    #PROFILE
    path('profile/view/<int:id>/', views.profile_view, name='profile'),
    path('api/usuario/<int:id>/actualizar_img/', views.actualizar_img_profile, name='actualizar_img_profile'),
    path('api/usuario/<int:id>/actualizar_banner/', views.actualizar_banner_profile, name='actualizar_banner_profile'),






]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
