from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView

from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from instrumento.models import Especie, Activo
from .models import Operacion
from .forms import NuevaOperacionForm
from .utils import (
    #get_unique_activos,
    #get_operaciones_resumen,
    get_operaciones_resultado,
    get_operaciones_tenencia,
)
from .tables import ResultadosTable, TenenciaTable, OperacionesTable
from django_tables2 import RequestConfig

import pandas as pd
import plotly.express as px
from django.shortcuts import render
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class UserCanEditOperacionMixin(LoginRequiredMixin):
    def check_user_permission(self, user):
        operacion = self.get_object()
        if operacion.user != user:
            raise Http404("No tienes permiso para acceder a esta operación.")

    def dispatch(self, request, *args, **kwargs):
        self.check_user_permission(request.user)
        return super().dispatch(request, *args, **kwargs)


class TenenciaView(LoginRequiredMixin, TemplateView):
    template_name = "cartera/tenencia.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        operaciones_tenencia = get_operaciones_tenencia(user)

        #print("operaciones_tenencia:", operaciones_tenencia)

        try:
            chart_data = pd.DataFrame(operaciones_tenencia)
            chart_data['activo'] = chart_data['activo'].astype(str)
            sunburst_data = chart_data.groupby(['tipo', 'activo'])['tenencia_usd'].sum().reset_index()
            chart_data['porcentaje'] = chart_data['tenencia_usd'] / chart_data['tenencia_usd'].sum()

            fig = px.sunburst(
                sunburst_data,
                path=['tipo', 'activo'],
                values='tenencia_usd',
                labels='etiquetas',
                title='Tenencia en USD',
            )
                
            fig.update_layout(
                title='Tenencia en USD',
                title_x=0.5,
                font=dict(size=14),
                margin=dict(l=20, r=20, t=30, b=5),
                height=550
            )

            fig.update_traces(texttemplate="<b>%{label}</b><br>%{value:,.0f} USD (%{percentRoot:.1%})", hovertemplate='<b>%{label}</b><br>%{value:,.2f} USD (%{percentRoot:.1%})')

            graph_html = fig.to_html(full_html=False)

        except Exception as e:
            error_message = str(e)
            print(f"Error: {error_message}")
            graph_html = "No hay datos para graficar"

        table = TenenciaTable(operaciones_tenencia, order_by=self.request.GET.get("sort"))
        context = {
            "tenencia": operaciones_tenencia,
            "table": table,
            "chart": graph_html
        }

        return context


class ResultadosView(LoginRequiredMixin, TemplateView):
    template_name = "cartera/resultados.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        operaciones_resultado = get_operaciones_resultado(user)

        try:
            tipo_colores = {
                'CEDEARS': 'blue',
                'ONS': 'crimson',
                'BONOS': 'green',
                'MERVAL': 'orange',
                'LETRAS': 'darkviolet',
            }
            colores = ['green', 'blue', 'darkviolet', 'orange', 'crimson', ]
            chart_data = pd.DataFrame(operaciones_resultado)
            chart_data['activo'] = chart_data['activo'].astype(str)
            print(chart_data)
            #chart_data_main = chart_data.groupby('tipo')['resultado_usd'].sum().reset_index()
            chart_data_sub = chart_data.groupby(['tipo', 'activo'])['resultado_usd'].sum().reset_index()
            fig = make_subplots(rows=2, cols=1, shared_xaxes=False, subplot_titles=["Tipos", "Activos"], vertical_spacing=0.10)

            # Gráfico por tipo
            tipo_data = chart_data.groupby('tipo')['resultado_usd'].sum().reset_index()
            fig.add_trace(go.Bar(x=tipo_data['tipo'], y=tipo_data['resultado_usd'], name='', marker_color=colores), row=1, col=1)

            # Gráfico por activo
            for tipo in chart_data_sub['tipo'].unique():
                data_tipo = chart_data_sub[chart_data_sub['tipo'] == tipo]
                fig.add_trace(go.Bar(x=data_tipo['activo'], y=data_tipo['resultado_usd'], name=tipo, marker_color=tipo_colores[tipo],), row=2, col=1)

            fig.update_layout(
                barmode='group',
                margin=dict(l=5, r=5, t=20, b=5),
                height=600
            )

            fig.update_yaxes(title_text="Resultado en USD", row=1, col=1)
            fig.update_yaxes(title_text="Resultado en USD", row=2, col=1)
            fig.update_xaxes(tickfont=dict(size=10), row=2, col=1)

            fig.update_traces(
                selector=dict(type='bar'), 
                showlegend=False,
                hovertemplate='%{x}: %{y:.2f} USD',
            )

            graph_html = pio.to_html(fig, include_plotlyjs=False, full_html=False)

        except Exception as e:
            error_message = str(e)
            print(f"Error: {error_message}")
            graph_html = "No hay datos para graficar"

        table = ResultadosTable(operaciones_resultado, order_by=self.request.GET.get("sort"))
        context = {
            "resultados": operaciones_resultado,
            "table": table,
            "chart": graph_html
        }
        return context


class OperacionesView(LoginRequiredMixin, View):
    template_name = "cartera/operaciones.html"
    login_url = '/login/' 

    def get(self, request, *args, **kwargs):
        user = self.request.user

        def get_data():
            queryset = Operacion.objects.filter(user=user)
            return queryset
        
        operaciones = get_data()

        table = OperacionesTable(get_data(), order_by=self.request.GET.get("sort"))
        RequestConfig(request, paginate=True).configure(table)

        context = {
            "table": table,
            "operaciones": operaciones,
        }

        return render(request, self.template_name, context)


class NuevaOperacionView(LoginRequiredMixin, CreateView):
    model = Operacion
    form_class = NuevaOperacionForm
    template_name = 'cartera/nueva_operacion.html'
    success_url = reverse_lazy('operaciones')
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        activos_en_tenencia = get_operaciones_tenencia(self.request.user)
        kwargs['activos_en_tenencia'] = activos_en_tenencia
        return kwargs

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
        #return super().form_invalid(form)
        # Si el formulario es inválido, vuelves a renderizar el mismo template con el formulario y los mensajes de error
        return self.render_to_response(self.get_context_data(form=form))



class EditarOperacionView(UserCanEditOperacionMixin, UpdateView):
    model = Operacion
    form_class = NuevaOperacionForm
    template_name = 'cartera/editar_operacion.html'
    success_url = reverse_lazy('operaciones')
    login_url = '/login/'  # URL de inicio de sesión, ajusta según tus configuraciones

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        operacion = self.get_object()
        activos_en_tenencia = get_operaciones_tenencia(self.request.user, operacion.id)
        kwargs['is_new'] = False  # Pasar is_new=False a NuevaOperacionForm
        kwargs['instance'] = operacion  # Pasar la instancia de la operación a editar
        kwargs['activos_en_tenencia'] = activos_en_tenencia
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
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class EliminarOperacionView(UserCanEditOperacionMixin, DeleteView):
    model = Operacion
    template_name = 'eliminar_operacion.html'
    success_url = reverse_lazy('operaciones')
    login_url = '/login/'

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


def detalle_activo_view(request, activo_id):
    user=request.user
    activo = get_object_or_404(Activo, pk=activo_id)
    operaciones = []

    if user.is_authenticated:
        operaciones = Operacion.objects.filter(user=user, activo=activo)

    especies_ars = Especie.objects.filter(activo=activo, moneda='ARS')
    especies_mep = Especie.objects.filter(activo=activo, moneda='MEP')
    especies_ccl = Especie.objects.filter(activo=activo, moneda='CCL')

    context = {
        'activo': activo,
        'especies_ars': especies_ars,
        'especies_mep': especies_mep,
        'especies_ccl': especies_ccl,
        'operaciones': operaciones,
    }

    return render(request, "detalle_activo.html", context)
