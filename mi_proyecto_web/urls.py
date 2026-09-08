from django.urls import path

from mi_proyecto_web import views


app_name = 'mi_proyecto_web'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.lista_productos, name='lista'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle'),
    path('producto/<int:producto_id>/comprar/', views.comprar_producto, name='comprar'),
    path('iniciar-sesion/', views.iniciar_sesion, name='login'),
    path('registro/', views.registrarse, name='registro'),
    path('cerrar-sesion/', views.cerrar_sesion, name='logout'),
]