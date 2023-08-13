from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Envía un correo electrónico de prueba.'

    def handle(self, *args, **options):
        subject = 'Prueba de correo electrónico'
        message = 'Este es un correo electrónico de prueba enviado desde el comando de Django.'
        from_email = 'cuentas@finanzars.com.ar'
        recipient_list = ['morellinicolas96@gmail.com']

        send_mail(subject, message, from_email, recipient_list)

        self.stdout.write(self.style.SUCCESS('Correo electrónico de prueba enviado correctamente.'))
