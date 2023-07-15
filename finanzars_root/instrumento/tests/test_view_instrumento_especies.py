from django.urls import reverse, resolve
from django.test import TestCase
from ..views import especies, nueva_especie
from ..models import Tipo, Especie

class EspeciesTests(TestCase):
    def setUp(self):
        tipo_instance, created = Tipo.objects.get_or_create(tipo="CEDEAR")
        Especie.objects.create(
            especie="Django",
            tipo=tipo_instance,
            nombre="test",
            plazo="48hs",
            apertura=100,
            ultimo=100,
            cierre_ant=100,
            var=0,
            hora="",
        )

    def test_especies_view_success_status_code(self):
        url = reverse("especies", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_especies_view_not_found_status_code(self):
        # check if the view is raising a 404 error when the Tipo does not exist
        url = reverse("especies", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_especies_url_resolves_especies_view(self):
        view = resolve("/instrumentos/1/")
        self.assertEquals(view.func, especies)

    def test_especies_view_contains_link_back_to_tipos(self):
        especies_url = reverse("especies", kwargs={"pk": 1})
        response = self.client.get(especies_url)
        tipos_url = reverse("tipos")
        self.assertContains(response, 'href="{0}"'.format(tipos_url))

    def test_especies_view_contains_navigation_links(self):
        especies_url = reverse("especies", kwargs={"pk": 1})
        tipos_url = reverse("tipos")
        nueva_especie_url = reverse("nueva_especie", kwargs={"pk": 1})

        response = self.client.get(especies_url)

        self.assertContains(response, 'href="{0}"'.format(tipos_url))
        self.assertContains(response, 'href="{0}"'.format(nueva_especie_url))
