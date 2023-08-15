from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .forms import RegistroForm

# Create your views here.


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            subject = 'Bienvenido a FinanzARS'
            context = {'username': user.username}
            html_message = render_to_string('cuentas/welcome_email.html', context)
            plain_message = strip_tags(html_message)  # Convertir HTML a texto plano
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

            return redirect("tipos")
    else:
        form = RegistroForm()
    return render(request, "cuentas/registro.html", {"form": form})
