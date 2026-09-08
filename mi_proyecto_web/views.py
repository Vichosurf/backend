import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Producto


PRODUCTOS_JSON = '''[
{"id":1,"nombre":"Martillo de uña 16 oz","categoria":"Herramientas","precio":8990,"stock":12},
{"id":2,"nombre":"Destornillador Phillips mediano","categoria":"Herramientas","precio":3990,"stock":25},
{"id":3,"nombre":"Alicate universal 8 pulgadas","categoria":"Herramientas","precio":7490,"stock":8},
{"id":4,"nombre":"Llave ajustable 10 pulgadas","categoria":"Herramientas","precio":9990,"stock":0},
{"id":5,"nombre":"Cinta métrica 5 metros","categoria":"Medición","precio":4990,"stock":31},
{"id":6,"nombre":"Nivel de burbuja 60 cm","categoria":"Medición","precio":10990,"stock":6},
{"id":7,"nombre":"Serrucho carpintero 20 pulgadas","categoria":"Herramientas","precio":12990,"stock":4},
{"id":8,"nombre":"Caja de herramientas 19 pulgadas","categoria":"Organización","precio":18990,"stock":10},
{"id":9,"nombre":"Taladro eléctrico 650 W","categoria":"Eléctricas","precio":45990,"stock":3},
{"id":10,"nombre":"Broca para concreto 8 mm","categoria":"Accesorios","precio":2490,"stock":40},
{"id":11,"nombre":"Broca para metal 6 mm","categoria":"Accesorios","precio":1990,"stock":0},
{"id":12,"nombre":"Disco de corte metal 4.5 pulgadas","categoria":"Accesorios","precio":1590,"stock":28},
{"id":13,"nombre":"Lija para madera grano 120","categoria":"Pintura","precio":890,"stock":55},
{"id":14,"nombre":"Rodillo para pintura 9 pulgadas","categoria":"Pintura","precio":3490,"stock":16},
{"id":15,"nombre":"Brocha plana 2 pulgadas","categoria":"Pintura","precio":2290,"stock":20},
{"id":16,"nombre":"Bandeja para pintura","categoria":"Pintura","precio":2990,"stock":0},
{"id":17,"nombre":"Esmalte al agua blanco 1 galón","categoria":"Pintura","precio":19990,"stock":7},
{"id":18,"nombre":"Silicona transparente 280 ml","categoria":"Adhesivos","precio":4590,"stock":14},
{"id":19,"nombre":"Pegamento para madera 250 g","categoria":"Adhesivos","precio":3990,"stock":9},
{"id":20,"nombre":"Cinta aisladora negra","categoria":"Electricidad","precio":1290,"stock":35},
{"id":21,"nombre":"Enchufe macho 10 A","categoria":"Electricidad","precio":1890,"stock":22},
{"id":22,"nombre":"Interruptor simple blanco","categoria":"Electricidad","precio":2490,"stock":18},
{"id":23,"nombre":"Ampolleta LED 9 W cálida","categoria":"Electricidad","precio":2990,"stock":26},
{"id":24,"nombre":"Alargador eléctrico 5 metros","categoria":"Electricidad","precio":8990,"stock":5},
{"id":25,"nombre":"Tubo PVC hidráulico 20 mm","categoria":"Plomería","precio":3290,"stock":13},
{"id":26,"nombre":"Codo PVC 20 mm","categoria":"Plomería","precio":590,"stock":44},
{"id":27,"nombre":"Llave de paso 1/2 pulgada","categoria":"Plomería","precio":5490,"stock":11},
{"id":28,"nombre":"Flexible para lavaplatos","categoria":"Plomería","precio":6990,"stock":0},
{"id":29,"nombre":"Teja asfáltica negra","categoria":"Construcción","precio":12990,"stock":21},
{"id":30,"nombre":"Saco de cemento 25 kg","categoria":"Construcción","precio":5990,"stock":30},
{"id":31,"nombre":"Guantes de trabajo reforzados","categoria":"Seguridad","precio":2990,"stock":19},
{"id":32,"nombre":"Lentes de seguridad transparentes","categoria":"Seguridad","precio":2490,"stock":24},
{"id":33,"nombre":"Mascarilla respiratoria","categoria":"Seguridad","precio":4990,"stock":0},
{"id":34,"nombre":"Chaleco reflectante talla única","categoria":"Seguridad","precio":7990,"stock":6},
{"id":35,"nombre":"Tornillo para madera 6 x 1 pulgadas","categoria":"Fijaciones","precio":2990,"stock":38},
{"id":36,"nombre":"Tarugo nylon 8 mm, 100 unidades","categoria":"Fijaciones","precio":3490,"stock":17},
{"id":37,"nombre":"Perno hexagonal 3/8 pulgadas","categoria":"Fijaciones","precio":790,"stock":32},
{"id":38,"nombre":"Cadena galvanizada por metro","categoria":"Fijaciones","precio":2290,"stock":0},
{"id":39,"nombre":"Escalera de aluminio 4 peldaños","categoria":"Jardinería","precio":39990,"stock":2},
{"id":40,"nombre":"Manguera de jardín 15 metros","categoria":"Jardinería","precio":14990,"stock":12}
]'''


IMAGENES_LOCAL = {
    1: 'imagenes/martillo-una-curva-16oz-truper.png',
    2: 'imagenes/destornillador-phillips-mediano.avif',
    3: 'imagenes/alicate-universal-8-pulgadas.png',
    4: 'imagenes/16a132ebc7063e3f.png',
    5: 'imagenes/Cinta_metrica_5_metros.jpg',
    6: 'imagenes/D_NQ_NP_975347-MLC87896095587_072025-O-nivel-de-burbuja-profesional-60cm-con-triple-medicion.webp',
    7: 'imagenes/serrucho-carpintero-20-pulgadas.jpg',
    8: 'imagenes/caja-herramientas-truper-cha-19nc.jpg',
    9: 'imagenes/540.webp',
    10: 'imagenes/044650.png',
    11: 'imagenes/w=1004,h=1500,fit=pad.webp',
    12: 'imagenes/D_NQ_NP_694873-MLA99557459670_122025-O.webp',
    13: 'imagenes/lija-para-madera-grano-100-30253005-1_7qhm1oxf7stetmbt.webp',
    14: 'imagenes/1200.webp',
    15: 'imagenes/D_790753-MLC50656203268_072022-F.jpg',
    16: 'imagenes/BANDEJA-509-RN-peq-copia.jpg',
    17: 'imagenes/EAA-MATE-1.png',
    18: 'imagenes/w=1500,h=1500,fit=cover.webp',
    19: 'imagenes/tekbond-cola-madeira-frontal.webp',
    20: 'imagenes/X_712d69szsvs-sx5226784.jpg',
    21: 'imagenes/X_template-bag-1-photoroom-2023-08-07t103148-1455335.png',
    22: 'imagenes/template-bag-1-photoroom-608881.jpg',
    23: 'imagenes/3012-1-ampolleta-led-e27-12v-24v-9w-3000k-faretto2057.jpg',
    24: 'imagenes/3786-1-alargador-de-5-metros-5-tomas-10a-blanco8703.jpg',
    25: 'imagenes/1440.webp',
    26: 'imagenes/247379-800-auto.webp',
    27: 'imagenes/ed855ba7-bb51-44f2-94a9-fbbe982d1497-f0b20f6f-9cb5-442c-af5a-8abab172f551-open-uri20221028-4063-1vf28j7_1024x1024.webp',
    28: 'imagenes/D_NQ_NP_981554-MLC73304956536_122023-O.webp',
    29: 'imagenes/Teja-negra.jpg',
    30: 'imagenes/public.webp',
    31: 'imagenes/guantes-mecanico-reforzado-truper.jpg',
    32: 'imagenes/lentes-seguridad-policarbonato-transparente-pretul.jpg',
    33: 'imagenes/mascarilla-3m-de-2-vias-6200.jpg',
    34: 'imagenes/w=1200,h=1400,fit=pad.webp',
    35: 'imagenes/crs9849.png',
    36: 'imagenes/1288486-0000-002.webp',
    37: 'imagenes/98711_20211126121310.jpg',
    38: 'imagenes/D_NQ_NP_811757-MLC82095023946_022025-O-cadena-eslabon-largo-10-milimetro-de-espesor-x-metro.webp',
    39: 'imagenes/escalera-aluminio-plegable-4-peldanos-jca-04.jpg',
    40: 'imagenes/1784735422026-MKHBNVCN16-1-1.webp'
}


def obtener_productos(request=None):
    if not Producto.objects.exists():
        productos_iniciales = json.loads(PRODUCTOS_JSON)
        Producto.objects.bulk_create([
            Producto(
                id=producto['id'],
                nombre=producto['nombre'],
                categoria=producto['categoria'],
                precio=producto['precio'],
                stock=producto['stock'],
                imagen=IMAGENES_LOCAL.get(producto['id'], ''),
            )
            for producto in productos_iniciales
        ])
    return Producto.objects.all()


def lista_productos(request):
    productos = obtener_productos(request)
    resumen = {
        'total': productos.count(),
        'disponibles': productos.filter(stock__gt=0).count(),
    }
    return render(request, 'mi_proyecto_web/lista.html', {
        'productos': productos,
        'resumen': resumen,
    })


def detalle_producto(request, producto_id):
    producto = get_object_or_404(obtener_productos(request), id=producto_id)
    return render(request, 'mi_proyecto_web/detalle.html', {'producto': producto})


@require_POST
@login_required(login_url='mi_proyecto_web:login')
def comprar_producto(request, producto_id):
    with transaction.atomic():
        producto = get_object_or_404(Producto.objects.select_for_update(), id=producto_id)
        try:
            cantidad = int(request.POST.get('cantidad', ''))
        except (TypeError, ValueError):
            cantidad = 0

        if producto.stock == 0:
            messages.error(request, 'Este producto ya no tiene stock disponible.')
        elif cantidad < 1:
            messages.error(request, 'Indica una cantidad válida para comprar.')
        elif producto.stock < cantidad:
            messages.error(request, f'Solo quedan {producto.stock} unidades disponibles.')
        else:
            producto.stock -= cantidad
            producto.save(update_fields=['stock'])
            messages.success(request, f'Compra realizada: {cantidad} unidad(es) de {producto.nombre}.')

    return redirect('mi_proyecto_web:detalle', producto_id=producto_id)


def inicio(request):
    productos = obtener_productos(request)
    destacados = productos.filter(stock__gt=0)[:3]
    return render(request, 'mi_proyecto_web/inicio.html', {'destacados': destacados})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('mi_proyecto_web:lista')
    if request.method == 'POST':
        usuario = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if usuario is not None:
            login(request, usuario)
            destino = request.POST.get('next') or request.GET.get('next')
            if destino and url_has_allowed_host_and_scheme(destino, {request.get_host()}, require_https=request.is_secure()):
                return redirect(destino)
            return redirect('mi_proyecto_web:lista')
        messages.error(request, 'El usuario o la contraseña no son correctos.')
    return render(request, 'mi_proyecto_web/login.html')


def registrarse(request):
    if request.user.is_authenticated:
        return redirect('mi_proyecto_web:lista')
    formulario = UserCreationForm(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save()
        login(request, usuario)
        return redirect('mi_proyecto_web:lista')
    return render(request, 'mi_proyecto_web/registro.html', {'formulario': formulario})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('mi_proyecto_web:inicio')