from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView

from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from instrumento.models import Tipo, Especie, Activo
from .models import Operacion
from .forms import NuevaOperacionForm
from .utils import (
    get_unique_activos,
    get_operaciones_resumen,
    get_operaciones_resultado,
    get_operaciones_tenencia,
)
from .tables import ResultadosTable, TenenciaTable, OperacionesTable
from django_tables2 import SingleTableView, RequestConfig


# Create your views here.
class TenenciaView(LoginRequiredMixin, TemplateView):
    template_name = "tenencia.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        activos = get_unique_activos(user)
        operaciones_resumen = get_operaciones_resumen(user)
        operaciones_resultado = get_operaciones_resultado(user)
        operaciones_tenencia = get_operaciones_tenencia(user)

        table = TenenciaTable(operaciones_tenencia, order_by=self.request.GET.get("sort"))
        context = {
            "activos": activos,
            "resumen": operaciones_resumen,
            "resultados": operaciones_resultado,
            "tenencia": operaciones_tenencia,
            "table": table,
        }

        return context

'''@login_required
def tenencia(request):
    user = request.user
    activos = get_unique_activos(user)
    operaciones_resumen = get_operaciones_resumen(user)
    operaciones_resultado = get_operaciones_resultado(user)
    operaciones_tenencia = get_operaciones_tenencia(user)

    table = TenenciaTable(operaciones_tenencia, order_by=request.GET.get("sort"))
    context = {
        "activos": activos,
        "resumen": operaciones_resumen,
        "resultados": operaciones_resultado,
        "tenencia": operaciones_tenencia,
        "table": table,
    }

    return render(request, "tenencia.html", context)
'''

class ResultadosView(LoginRequiredMixin, TemplateView):
    template_name = "resultados.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        activos = get_unique_activos(user)
        operaciones_resumen = get_operaciones_resumen(user)
        operaciones_resultado = get_operaciones_resultado(user)

        table = ResultadosTable(operaciones_resultado, order_by=self.request.GET.get("sort"))
        context = {
            "activos": activos,
            "resumen": operaciones_resumen,
            "resultados": operaciones_resultado,
            "table": table,
        }
        return context

'''@login_required
def resultados(request):
    user = request.user
    activos = get_unique_activos(user)
    operaciones_resumen = get_operaciones_resumen(user)
    operaciones_resultado = get_operaciones_resultado(user)

    table = ResultadosTable(operaciones_resultado, order_by=request.GET.get("sort"))
    context = {
        "activos": activos,
        "resumen": operaciones_resumen,
        "resultados": operaciones_resultado,
        "table": table,
    }

    return render(request, "resultados.html", context)
'''

class OperacionesView(LoginRequiredMixin, View):
    template_name = "operaciones.html"
    login_url = '/login/' 

    def get(self, request, *args, **kwargs):
        user = self.request.user

        def get_data():
            queryset = Operacion.objects.filter(user=user)
            return queryset

        table = OperacionesTable(get_data(), order_by=self.request.GET.get("sort"))
        RequestConfig(request, paginate=True).configure(table)

        context = {
            "table": table,
        }

        return render(request, self.template_name, context)

'''@login_required
def operaciones(request):
    user = request.user

    def get_data():
        queryset = Operacion.objects.filter(user=user)
        return queryset

    table = OperacionesTable(get_data(), order_by=request.GET.get("sort"))
    RequestConfig(request, paginate=True).configure(table)

    context = {
        "table": table,
    }

    return render(request, "operaciones.html", context)
'''

class NuevaOperacionView(LoginRequiredMixin, CreateView):
    model = Operacion
    form_class = NuevaOperacionForm
    template_name = 'nueva_operacion.html'
    success_url = reverse_lazy('tenencia')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


'''@login_required
def nueva_operacion(request):
    user = User.objects.first()
    tipo = Tipo.objects.all()
    activo = Activo.objects.all()
    especie = Especie.objects.all()

    if request.method == "POST":
        form = NuevaOperacionForm(request.POST)
        if form.is_valid():
            operacion = form.save(commit=False)
            operacion.plazo = form.cleaned_data.get("plazo")
            operacion.user = user
            operacion.tipo = form.cleaned_data.get("tipo")
            operacion.activo = form.cleaned_data.get("activo")
            operacion.especie = form.cleaned_data.get("especie")
            operacion.fecha = form.cleaned_data.get("fecha")
            operacion.cotiz_mep = form.cleaned_data.get("cotiz_mep")
            operacion.operacion = form.cleaned_data.get("operacion")
            operacion.cantidad = form.cleaned_data.get("cantidad")
            operacion.precio_ars = form.cleaned_data.get("precio_ars")
            operacion.precio_usd = form.cleaned_data.get("precio_usd")
            operacion.save()

            return redirect("tenencia")

    else:
        form = NuevaOperacionForm()

    return render(
        request,
        "nueva_operacion.html",
        {"tipo": tipo, "especie": especie, "activo": activo, "form": form},
    )
'''

class EditarOperacionView(LoginRequiredMixin, UpdateView):
    model = Operacion
    form_class = NuevaOperacionForm
    template_name = 'editar_operacion.html'
    success_url = reverse_lazy('operaciones')
    login_url = '/login/'  # URL de inicio de sesión, ajusta según tus configuraciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operacion = self.get_object()
        context['tipo'] = operacion.tipo
        form = context['form']
        form.fields['activo'].queryset = operacion.tipo.activos.order_by('ticker_ars')
        return context

'''@login_required
def editar_operacion(request, pk):
    operacion = get_object_or_404(Operacion, pk=pk)
    tipo = operacion.tipo
    activo = operacion.activo

    if request.method == "POST":
        form = NuevaOperacionForm(request.POST, instance=operacion)
        if form.is_valid():
            form.save()
            return redirect("operaciones")
    else:
        form = NuevaOperacionForm(instance=operacion)

    form.fields["activo"].queryset = tipo.activos.order_by("ticker_ars")

    return render(request, "editar_operacion.html", {"form": form,})
'''

class EliminarOperacionView(LoginRequiredMixin, DeleteView):
    model = Operacion
    template_name = 'eliminar_operacion.html'
    success_url = reverse_lazy('operaciones')
    login_url = '/login/'  # URL de inicio de sesión, ajusta según tus configuraciones

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

'''@login_required
def eliminar_operacion(request, pk):
    operacion = get_object_or_404(Operacion, pk=pk)
    
    if request.method == 'POST':
        operacion.delete()
        return redirect("operaciones")

    #context = {'operacion': operacion}

    return redirect("operaciones",)
    #return render(request, "operaciones.html", context)
'''

def load_activos(request):
    tipo_id = request.GET.get("tipo")
    activos = Activo.objects.filter(tipo_id=tipo_id).order_by("ticker_ars")
    return render(request, "hr/activo_dropdown_list_options.html", {"activos": activos})

def load_activo_name(request):
    activo_id = request.GET.get("activo")
    nombre_activo = Activo.objects.filter(id=activo_id)[0].nombre
    return render(request, "hr/nombre_activo_label.html", {"nombre_activo": nombre_activo})

def load_especies(request):
    activo_id = request.GET.get("activo")
    plazo = request.GET.get("plazo")
    especies = Especie.objects.filter(activo_id=activo_id, plazo=plazo).order_by(
        "especie"
    )
    return render(
        request, "hr/especie_dropdown_list_options.html", {"especies": especies}
    )

def load_mep(request):
    mep = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
    return JsonResponse(mep, safe=False)