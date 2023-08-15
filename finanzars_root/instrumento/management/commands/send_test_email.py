from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

'''
class Command(BaseCommand):
    help = 'Envía un correo electrónico de prueba.'

    def handle(self, *args, **options):
        subject = 'Prueba de correo electrónico'
        message = 'Este es un correo electrónico de prueba enviado desde el comando de Django.'
        from_email = 'cuentas@finanzars.com.ar'
        recipient_list = ['morellinicolas96@gmail.com']

        send_mail(subject, message, from_email, recipient_list)

        self.stdout.write(self.style.SUCCESS('Correo electrónico de prueba enviado correctamente.'))
'''

class Command(BaseCommand):
    help = 'Envía un correo electrónico de prueba.'

    def handle(self, *args, **options):
        subject = 'Prueba de correo electrónico'
        html_message = render_to_string('cuentas/welcome_email.html')
        plain_message = strip_tags(html_message)  # Convertir HTML a texto plano
        from_email = 'cuentas@finanzars.com.ar'
        recipient_list = ['morellinicolas96@gmail.com']

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        self.stdout.write(self.style.SUCCESS('Correo electrónico de prueba enviado correctamente.'))
