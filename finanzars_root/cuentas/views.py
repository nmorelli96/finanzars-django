from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
#from django.http import Http404

from .forms import RegistroForm, ModificarDatosForm
from cartera.models import Operacion
from cuentas.models import UserProfile


# class UserPermissionRequiredMixin(LoginRequiredMixin):
#     def check_user_permission(self, user):
#         if self.get_object() != user:
#             raise Http404("No tienes permiso para acceder a esta página.")

#     def dispatch(self, request, *args, **kwargs):
#         self.check_user_permission(request.user)
#         return super().dispatch(request, *args, **kwargs)


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

            return redirect("home")
    else:
        form = RegistroForm()

    return render(request, "cuentas/registro.html", {"form": form})


@login_required
def mi_cuenta(request):
    user = request.user
    operaciones_count = Operacion.objects.filter(user=user).count()
    user_profile = UserProfile.objects.filter(user=user).first()
    context = {
        'user_detail': user,
        'operaciones_count': operaciones_count,
        'user_profile': user_profile,
    }
    return render(request, 'cuentas/mi_cuenta.html', context)


@login_required
def update_user(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ModificarDatosForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            profile_picture_url = form.cleaned_data['profile_picture_url']
            if not user_profile.profile_picture_url:
                user_profile.profile_picture_url = 'https://i.imgur.com/nkeHzfl.png'
            else:
                user_profile.profile_picture_url = profile_picture_url
            user_profile.save()

            return redirect('mi_cuenta')
    else:
        form = ModificarDatosForm(instance=request.user)

    return render(request, 'cuentas/update_user.html', {'form': form})
