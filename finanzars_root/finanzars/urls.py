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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views.generic import TemplateView

from instrumento import views
from cuentas import views as cuentas_views
from cartera import views as cartera_views
from dolar import views as dolar_views
from simuladores import views as sim_views

handler404 = views.handler404

from instrumento.management.commands.tasks import (
    actualizar_bonos,
    actualizar_cedears,
    actualizar_letras,
    actualizar_merval,
    actualizar_ons,
    actualizar_usa,
    actualizar_dolar,
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

scheduler.add_job(
    actualizar_bonos,
    trigger=CronTrigger(day_of_week="mon-fri", hour="11-18", minute="11-51/20"),
    id="actualizar_bonos",
    name="Actualizar Bonos",
    replace_existing=True,
    misfire_grace_time=30,
)

scheduler.add_job(
    actualizar_cedears,
    trigger=CronTrigger(day_of_week="mon-fri", hour="11-18", minute="12-52/20"),
    id="actualizar_cedears",
    name="Actualizar CEDEARS",
    replace_existing=True,
    misfire_grace_time=30,
)

scheduler.add_job(
    actualizar_letras,
    trigger=CronTrigger(day_of_week="mon-fri", hour="11-18", minute="18-58/20"),
    id="actualizar_letras",
    name="Actualizar Letras",
    replace_existing=True,
    misfire_grace_time=30,
)

scheduler.add_job(
    actualizar_merval,
    trigger=CronTrigger(day_of_week="mon-fri", hour="11-18", minute="14-54/20"),
    id="actualizar_merval",
    name="Actualizar Merval",
    replace_existing=True,
    misfire_grace_time=30,
)

scheduler.add_job(
    actualizar_ons,
    trigger=CronTrigger(day_of_week="mon-fri", hour="11-18", minute="16-56/20"),
    id="actualizar_ons",
    name="Actualizar ONS",
    replace_existing=True,
    misfire_grace_time=30,
)

scheduler.add_job(
    actualizar_usa,
    trigger=CronTrigger(day_of_week="mon-fri", hour="18"),
    id="actualizar_usa",
    name="Actualizar USA",
    replace_existing=True,
    misfire_grace_time=30,
)

scheduler.add_job(
    actualizar_dolar,
    trigger=CronTrigger(minute="*/10"),
    id="actualizar_dolar",
    name="Actualizar Dolar",
    replace_existing=True,
    misfire_grace_time=30,
)

scheduler.start()


urlpatterns = [
    path("", views.TiposView.as_view(), name="tipos"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("cuenta/", cuentas_views.mi_cuenta, name="mi_cuenta"),
    path("cuenta/modificar/", cuentas_views.update_user, name="modificar_datos"),
    path("registro/", cuentas_views.registro, name="registro"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="cuentas/login.html"),
        name="login",
    ),
    re_path(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "reset/",
        auth_views.PasswordResetView.as_view(
            template_name="cuentas/password_reset.html",
            email_template_name="cuentas/password_reset_email.html",
            subject_template_name="cuentas/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="cuentas/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="cuentas/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="cuentas/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "settings/password/",
        auth_views.PasswordChangeView.as_view(
            template_name="cuentas/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "settings/password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="cuentas/password_change_done.html"
        ),
        name="password_change_done",
    ),
    re_path(
        r"^instrumentos/(?P<pk>\d+)/$", views.EspeciesView.as_view(), name="especies"
    ),
    # re_path(
    #    r"^instrumentos/(?P<pk>\d+)/new/$", views.NuevaEspecieView.as_view(), name="nueva_especie"
    # ),
    path(
        "instrumentos/activo/<int:activo_id>",
        cartera_views.detalle_activo_view,
        name="detalle_activo",
    ),
    path("agregar_a_watchlist", views.add_favorito, name="agregar_favorito"),
    path("eliminar_de_watchlist", views.delete_favorito, name="eliminar_favorito"),
    path("get_watchlists_data", views.get_watchlists_data, name="get_watchlists_data"),
    path("instrumentos/usa", views.EspeciesUsaView.as_view(), name="especies_usa"),
    path(
        "instrumentos/comparador", views.comparador_cedears, name="comparador_cedears"
    ),
    path("watchlists/", views.display_watchlists, name="watchlists"),
    path(
        "watchlists/<int:watchlist_id>/eliminar",
        views.delete_watchlist,
        name="eliminar_watchlist",
    ),
    path(
        "watchlists/<int:watchlist_id>/editar",
        views.edit_watchlist,
        name="editar_watchlist",
    ),
    path("cuotas", sim_views.cuotas, name="cuotas"),
    path("prestamos", sim_views.prestamos, name="prestamos"),
    path(
        "cartera/operaciones/nueva",
        cartera_views.NuevaOperacionView.as_view(),
        name="nueva_operacion",
    ),
    re_path(
        r"^cartera/operaciones/editar/(?P<pk>\d+)$",
        cartera_views.EditarOperacionView.as_view(),
        name="editar_operacion",
    ),
    path(
        "cartera/operaciones/eliminar/<int:pk>",
        cartera_views.EliminarOperacionView.as_view(),
        name="eliminar_operacion",
    ),
    path(
        "cartera/operaciones/",
        cartera_views.OperacionesView.as_view(),
        name="operaciones",
    ),
    path(
        "cartera/resultados", cartera_views.ResultadosView.as_view(), name="resultados"
    ),
    path("cartera/tenencia", cartera_views.TenenciaView.as_view(), name="tenencia"),
    path("dolar", dolar_views.DolarView, name="dolar"),
    path("update-dolar-data", dolar_views.DolarFetch, name="update-dolar-data"),
    path(
        "update-especies-data", views.update_especies_data, name="update-especies-data"
    ),
    path("ajax/load-activos", cartera_views.load_activos, name="ajax_load_activos"),
    path("ajax/load-especies", cartera_views.load_especies, name="ajax_load_especies"),
    path(
        "ajax/load-activo-name",
        cartera_views.load_activo_name,
        name="ajax_load_activo_name",
    ),
    path("load-mep", cartera_views.load_mep, name="load_mep"),
    path("admin/", admin.site.urls),
]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
