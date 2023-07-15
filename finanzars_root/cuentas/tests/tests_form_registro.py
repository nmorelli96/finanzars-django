from django.test import TestCase
from ..forms import RegistroForm

class RegistroFormTest(TestCase):
    def test_form_has_fields(self):
        form = RegistroForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
