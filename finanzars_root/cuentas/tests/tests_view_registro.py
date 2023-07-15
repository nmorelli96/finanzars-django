from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from ..views import registro
from ..forms import RegistroForm


# Create your tests here.
class RegistroTests(TestCase):
    def setUp(self):
        url = reverse("registro")
        self.response = self.client.get(url)

    def test_registro_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_registro_url_resolves_registro_view(self):
        view = resolve("/registro/")
        self.assertEquals(view.func, registro)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, RegistroForm)

    def test_form_inputs(self):
        """
        The view must contain five inputs: csrf, username, email,
        password1, password2
        """
        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulRegistroTests(TestCase):
    def setUp(self):
        url = reverse("registro")
        data = {
            "username": "john",
            "email": "john@doe.com",
            "password1": "abcdef123456",
            "password2": "abcdef123456",
        }
        self.response = self.client.post(url, data)
        self.tipos_url = reverse("tipos")

    def test_redirection(self):
        """
        A valid form submission should redirect the user to the home page
        """
        self.assertRedirects(self.response, self.tipos_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        """
        response = self.client.get(self.tipos_url)
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)


class InvalidRegistroTests(TestCase):
    def setUp(self):
        url = reverse("registro")
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_registro_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
