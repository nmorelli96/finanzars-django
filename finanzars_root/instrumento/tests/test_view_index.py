from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.models import User
from ..views import tipos, especies, nueva_especie
from ..models import Tipo, Especie

class HomeTests(TestCase):
    def setUp(self):  # creates a Board instance to be used during the tests
        self.tipo = Tipo.objects.create(tipo="Django")
        url = reverse("tipos")
        self.response = self.client.get(url)

    def test_tipos_view_status_code(self):
        # We are testing the status code of the response. The status code 200 means success.
        self.assertEquals(self.response.status_code, 200)

    def test_tipos_url_resolves_tipos_view(self):
        # check if the right view is being used
        view = resolve("/")
        self.assertEquals(view.func, tipos)

    def test_tipos_view_contains_link_to_especies_page(self):
        # ensure the navigation back to the list of topics
        especies_url = reverse("especies", kwargs={"pk": self.tipo.pk})
        self.assertContains(self.response, 'href="{0}"'.format(especies_url))
