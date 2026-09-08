from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Producto


class CatalogoTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Producto de prueba',
            categoria='Herramientas',
            precio=1000,
            stock=2,
        )
        self.usuario = get_user_model().objects.create_user(
            username='cliente',
            password='ClaveSegura123!',
        )

    def test_landing_catalogo_y_detalle_cargan(self):
        self.assertEqual(self.client.get(reverse('mi_proyecto_web:inicio')).status_code, 200)
        self.assertEqual(self.client.get(reverse('mi_proyecto_web:lista')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('mi_proyecto_web:detalle', args=[self.producto.id])).status_code,
            200,
        )

    def test_compra_requiere_inicio_de_sesion(self):
        url = reverse('mi_proyecto_web:comprar', args=[self.producto.id])
        response = self.client.post(url)
        self.assertRedirects(response, f'{reverse("mi_proyecto_web:login")}?next={url}')
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 2)

    def test_usuario_puede_hacer_pseudocompra(self):
        self.client.force_login(self.usuario)
        response = self.client.post(
            reverse('mi_proyecto_web:comprar', args=[self.producto.id]),
            {'cantidad': 2},
        )
        self.assertRedirects(response, reverse('mi_proyecto_web:detalle', args=[self.producto.id]))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 0)

    def test_compra_no_supera_el_stock(self):
        self.client.force_login(self.usuario)
        response = self.client.post(
            reverse('mi_proyecto_web:comprar', args=[self.producto.id]),
            {'cantidad': 3},
            follow=True,
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 2)
        self.assertContains(response, 'Solo quedan 2 unidades disponibles.', status_code=200)

    def test_registro_y_login_cargan(self):
        self.assertEqual(self.client.get(reverse('mi_proyecto_web:login')).status_code, 200)
        self.assertEqual(self.client.get(reverse('mi_proyecto_web:registro')).status_code, 200)

    def test_producto_inexistente_devuelve_404(self):
        response = self.client.get(reverse('mi_proyecto_web:detalle', args=[9999]))
        self.assertEqual(response.status_code, 404)
