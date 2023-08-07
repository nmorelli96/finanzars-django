from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from instrumento.models import Especie, Activo
from .models import Operacion
from .forms import NuevaOperacionForm
from .utils import (
    get_unique_activos,
    get_operaciones_resumen,
    get_operaciones_resultado,
    get_operaciones_tenencia,
)
from .tables import ResultadosTable, TenenciaTable, OperacionesTable
from django_tables2 import RequestConfig


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


class NuevaOperacionView(LoginRequiredMixin, CreateView):
    model = Operacion
    form_class = NuevaOperacionForm
    template_name = 'nueva_operacion.html'
    success_url = reverse_lazy('operaciones')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        operacion = form.cleaned_data.get('operacion')

        if operacion in ['Venta', 'Compra']:
            form.instance.total_ars = 0
            form.instance.total_usd = 0
            if form.instance.operacion == 'Venta':
                form.instance.cantidad = -abs(form.instance.cantidad)
        else:
            # Si la operación no es 'Venta' ni 'Compra', omitir los campos cantidad, precio_ars y precio_usd
            form.instance.cantidad = 0
            form.instance.precio_ars = 0
            form.instance.precio_usd = 0
            form.instance.total_ars = -abs(form.instance.total_ars)
            form.instance.total_usd = -abs(form.instance.total_usd)

        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Captura el error y registra los errores del formulario en la consola del servidor
        print(form.errors)
        # Devuelve la respuesta por defecto que muestra los errores en el formulario
        return super().form_invalid(form)



class EditarOperacionView(LoginRequiredMixin, UpdateView):
    model = Operacion
    form_class = NuevaOperacionForm
    template_name = 'editar_operacion.html'
    success_url = reverse_lazy('operaciones')
    login_url = '/login/'  # URL de inicio de sesión, ajusta según tus configuraciones

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        operacion = self.get_object()
        kwargs['is_new'] = False  # Pasar is_new=False a NuevaOperacionForm
        kwargs['instance'] = operacion  # Pasar la instancia de la operación a editar
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operacion = self.get_object()
        context['tipo'] = operacion.tipo
        form = context['form']

        form.fields['tipo'].initial = operacion.tipo
        form.fields['activo'].queryset = operacion.tipo.activos.order_by('ticker_ars')
        form.fields['activo'].initial = operacion.activo
        form.fields['especie'].initial = operacion.especie
        form.fields['fecha'].initial = operacion.fecha
        form.fields['cotiz_mep'].initial = operacion.cotiz_mep
        form.fields['operacion'].initial = operacion.operacion
        form.fields['precio_ars'].initial = operacion.precio_ars
        form.fields['precio_usd'].initial = operacion.precio_usd

        if operacion.operacion == "Venta":
            form.fields['cantidad'].initial = -operacion.cantidad

        else:
            form.fields['cantidad'].initial = operacion.cantidad

        return context
    
    def form_valid(self, form):
        operacion = form.cleaned_data.get('operacion')

        if operacion in ['Venta', 'Compra']:
            form.instance.total_ars = 0
            form.instance.total_usd = 0
            if form.instance.operacion == 'Venta':
                form.instance.cantidad = -abs(form.instance.cantidad)
        else:
            # Si la operación no es 'Venta' ni 'Compra', omitir los campos cantidad, precio_ars y precio_usd
            form.instance.cantidad = 0
            form.instance.precio_ars = 0
            form.instance.precio_usd = 0
            form.instance.total_ars = -abs(form.instance.total_ars)
            form.instance.total_usd = -abs(form.instance.total_usd)

        return super().form_valid(form)


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

def load_activos(request):
    tipo_id = request.GET.get("tipo")
    activos = Activo.objects.filter(tipo_id=tipo_id).order_by("ticker_ars")
    return render(request, "includes/activo_dropdown_list_options.html", {"activos": activos})

def load_activo_name(request):
    activo_id = request.GET.get("activo")
    nombre_activo = Activo.objects.filter(id=activo_id)[0].nombre
    return render(request, "includes/nombre_activo_label.html", {"nombre_activo": nombre_activo})

def load_especies(request):
    activo_id = request.GET.get("activo")
    plazo = request.GET.get("plazo")
    especies = Especie.objects.filter(activo_id=activo_id, plazo=plazo).order_by(
        "especie"
    )
    return render(
        request, "includes/especie_dropdown_list_options.html", {"especies": especies}
    )

def load_mep(request):
    mep = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
    return JsonResponse(mep, safe=False)