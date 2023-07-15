from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.models import User
from ..views import especies, nueva_especie
from ..models import Tipo, Especie
from ..forms import NuevaEspecieForm

class NewEspecieTests(TestCase):
    def setUp(self):
        Tipo.objects.create(tipo="DJANGO")
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')

    def test_nueva_especie_view_success_status_code(self):
        url = reverse("nueva_especie", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_nueva_especie_view_not_found_status_code(self):
        url = reverse("nueva_especie", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_nueva_especie_url_resolves_nueva_especie_view(self):
        view = resolve("/instrumentos/1/new/")
        self.assertEquals(view.func, nueva_especie)

    def test_nueva_especie_view_contains_link_back_to_especies_view(self):
        nueva_especie_url = reverse("nueva_especie", kwargs={"pk": 1})
        especies_url = reverse("especies", kwargs={"pk": 1})
        response = self.client.get(nueva_especie_url)
        self.assertContains(response, 'href="{0}"'.format(especies_url))

    def test_csrf(self):
        url = reverse("nueva_especie", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_nueva_especie_valid_post_data(self):
        url = reverse("nueva_especie", kwargs={"pk": 1})
        tipo_instance, created = Tipo.objects.get_or_create(tipo="DJANGO")
        data = {
            "especie": "TEST",
            "tipo": tipo_instance.pk,
            "nombre": "",
            "plazo": "48hs",
            "apertura": 0,
            "ultimo": 0,
            "cierre_ant": 0,
            "var": 0,
            "hora": "17",
        }
        response = self.client.post(url, data)
        self.assertTrue(Especie.objects.exists())

    def test_nueva_especie_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        url = reverse("nueva_especie", kwargs={"pk": 1})
        response = self.client.post(url, {})
        form = response.context.get("form")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_nueva_especie_invalid_post_data_empty_fields(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        url = reverse("nueva_especie", kwargs={"pk": 1})
        data = {
            "especie": "",
            "tipo": "",
            "nombre": "",
            "plazo": "",
            "apertura": "",
            "ultimo": "",
            "cierre_ant": "",
            "var": "",
            "hora": "",
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Especie.objects.exists())

    def test_contains_form(self):
        url = reverse("nueva_especie", kwargs={"pk": 1})
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, NuevaEspecieForm)

class LoginRequiredNewTopicTests(TestCase):
    #make a request to the new topic view without being authenticated. 
    # The expected result is for the request be redirected to the login view.
    def setUp(self):
        Tipo.objects.create(tipo='DJANGO')
        self.url = reverse('nueva_especie', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
