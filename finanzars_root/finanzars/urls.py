"""
URL configuration for finanzars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from instrumento import views
from cuentas import views as cuentas_views
from cartera import views as cartera_views


urlpatterns = [
    path("", views.TiposView.as_view(), name="tipos"),
    path("registro/", cuentas_views.registro, name="registro"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    re_path(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            email_template_name="password_reset_email.html",
            subject_template_name="password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "settings/password/",
        auth_views.PasswordChangeView.as_view(template_name="password_change.html"),
        name="password_change",
    ),
    path(
        "settings/password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("contact/", views.contact, name="contact"),
    re_path(r"^instrumentos/(?P<pk>\d+)/$", views.EspeciesView.as_view(), name="especies"),
    re_path(
        r"^instrumentos/(?P<pk>\d+)/new/$", views.NuevaEspecieView.as_view(), name="nueva_especie"
    ),
    path("cartera/operaciones/nueva/", cartera_views.NuevaOperacionView.as_view(), name="nueva_operacion"),
    re_path(r"^cartera/operaciones/editar/(?P<pk>\d+)/$", cartera_views.EditarOperacionView.as_view(), name="editar_operacion"),
    path('cartera/operaciones/eliminar/<int:pk>/', cartera_views.EliminarOperacionView.as_view(), name='eliminar_operacion'),
    path("cartera/operaciones", cartera_views.OperacionesView.as_view(), name="operaciones"),
    path("cartera/resultados", cartera_views.ResultadosView.as_view(), name="resultados"),
    path("cartera/tenencia", cartera_views.TenenciaView.as_view(), name="tenencia"),
    path('ajax/load-activos/', cartera_views.load_activos, name='ajax_load_activos'),
    path('ajax/load-especies/', cartera_views.load_especies, name='ajax_load_especies'),
    path('ajax/load-activo-name/', cartera_views.load_activo_name, name='ajax_load_activo_name'),
    path("admin/", admin.site.urls),
]

#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
