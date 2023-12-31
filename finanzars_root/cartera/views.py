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
from .tables import ResultadosTable, TenenciaTable, OperacionesTable, OperacionesFilter
from django_tables2 import RequestConfig
from django_filters.views import FilterView 
from datetime import datetime

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
            colores = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
            tipo_colores = {
                'CEDEARS': colores[1],
                'ONS': colores[0],
                'BONOS': colores[4],
                'MERVAL': colores[2],
                'LETRAS': colores[3],
            }
            chart_data = pd.DataFrame(operaciones_resultado)
            chart_data['activo'] = chart_data['activo'].astype(str)
            #chart_data_main = chart_data.groupby('tipo')['resultado_usd'].sum().reset_index()
            chart_data_sub = chart_data.groupby(['tipo', 'activo'])['resultado_usd'].sum().reset_index()

            # Subplot de tipos
            tipo_data = chart_data.groupby('tipo')['resultado_usd'].sum().reset_index()
            tipo_data = tipo_data.sort_values(by='resultado_usd', ascending=False)
            tipos = tipo_data['tipo'].unique()
            fig = make_subplots(rows=len(tipos) + 2, 
                                cols=1, 
                                shared_xaxes=False, 
                                subplot_titles=["Resultado en USD por tipo y activos"], 
                                vertical_spacing=0.045)
            
            fig.add_trace(go.Bar(
                x=tipo_data['tipo'], 
                y=tipo_data['resultado_usd'], 
                name='', 
                marker_color=[tipo_colores[tipo] for tipo in tipo_data['tipo']],
                textfont=dict(family='roboto'),
                textposition='auto',
                text=round(tipo_data['resultado_usd'], 2).astype(str),
                ),
                row=1, 
                col=1
            )
            
            # Subplot de todos los activos
            for tipo in tipo_data['tipo'].unique():
                data_tipo = chart_data_sub[chart_data_sub['tipo'] == tipo]
                data_tipo = data_tipo.sort_values(by='resultado_usd', ascending=False)
                fig.add_trace(go.Bar(
                    x=data_tipo['activo'], 
                    y=data_tipo['resultado_usd'], 
                    name=tipo, 
                    marker_color=tipo_colores[tipo],
                    ), 
                    row=2, col=1
                )

            # Subplots de activos por tipo
            for i, tipo in enumerate(tipos, start=2):
                data_tipo = chart_data_sub[chart_data_sub['tipo'] == tipo]
                data_tipo = data_tipo.sort_values(by='resultado_usd', ascending=False)
                tipo_trace = go.Bar(
                    x=data_tipo['activo'], 
                    y=data_tipo['resultado_usd'], 
                    name=tipo, 
                    marker_color=tipo_colores[tipo],
                    textfont=dict(family='roboto'),
                    textposition='auto',
                    text=round(data_tipo['resultado_usd'], 2).astype(str),
                )
                fig.add_trace(tipo_trace, row=i + 1, col=1)

            fig.update_layout(
                barmode='group',
                margin=dict(l=8, r=8, t=25, b=5),
                height=250 * len(tipos),
            )

            fig.update_xaxes(tickfont=dict(family='roboto'))
            fig.update_yaxes(tickfont=dict(family='roboto'))

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


class OperacionesView(LoginRequiredMixin, FilterView):
    template_name = "cartera/operaciones.html"
    login_url = '/login/' 
    filterset_class = OperacionesFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tipo_filter = self.request.GET.get('tipo')
        operacion_filter = self.request.GET.get('operacion')
        activo_filter = self.request.GET.get('activo')
        fecha_desde_filter = self.request.GET.get('fecha_desde')
        fecha_hasta_filter = self.request.GET.get('fecha_hasta')

        queryset = Operacion.objects.filter(user=user)

        if tipo_filter:
            queryset = queryset.filter(tipo=tipo_filter)
        if operacion_filter:
            queryset = queryset.filter(operacion=operacion_filter)
        if activo_filter:
            queryset = queryset.filter(activo__ticker_ars__icontains=activo_filter)
        if fecha_desde_filter:
            fecha_desde = datetime.strptime(fecha_desde_filter, '%Y-%m-%d')
            queryset = queryset.filter(fecha__gte=fecha_desde)

        if fecha_hasta_filter:
            fecha_hasta = datetime.strptime(fecha_hasta_filter, '%Y-%m-%d')
            queryset = queryset.filter(fecha__lte=fecha_hasta)

        operaciones = queryset

        table = OperacionesTable(queryset, order_by=self.request.GET.get("sort"))
        RequestConfig(self.request, paginate=True).configure(table)

        context['filter'] = self.filterset_class(
            self.request.GET,
            queryset=queryset,
        )

        context['table'] = table
        context['operaciones'] = operaciones

        return context


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
