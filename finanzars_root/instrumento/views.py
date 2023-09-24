from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.template import loader

from .models import Tipo, Activo, Especie, Especie_USA, Nasdaq_Data
from cuentas.models import Watchlist
from .forms import NuevaEspecieForm
from cuentas.forms import WatchlistForm

from django_filters.views import FilterView 
from .tables import EspeciesTable, TiposTable, EspecieFilter, EspeciesUsaTable, ComparadorTable
from django_tables2 import SingleTableView, RequestConfig

from instrumento.management.commands.import_to_database import import_to_database_usa

import warnings
import json
from decouple import config

NASDAQ_DATA_TOKEN = config("NASDAQ_DATA_TOKEN")

warnings.filterwarnings("ignore", "DateTimeField .* received a naive datetime .* while time zone support is active.", RuntimeWarning)


def handler404(request, exception):
    return render(request, '404.html', status=404)


def sitemap(request):
    sitemap = loader.render_to_string('sitemap.xml')
    return HttpResponse(sitemap, content_type='application/xml')


class TiposView(SingleTableView):

    model = Tipo
    table_class = TiposTable
    #success_url = reverse_lazy('tipos')
    template_name = "tipos.html"
    


class EspeciesView(SingleTableView, FilterView):
    model = Especie
    table_class = EspeciesTable
    template_name = "especies.html"
    #paginator_class = LazyPaginator
    #paginate_by = 50
    filterset_class = EspecieFilter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = get_object_or_404(Tipo, pk=self.kwargs['pk'])
        queryset = context['tipo'].especies.all()
        plazo_filter = self.request.GET.get('plazo')
        hora_filter = self.request.GET.get('hora')
        especie_filter = self.request.GET.get('especie')

        # Filtrar especies vigentes (no vencidas)
        queryset = queryset.filter(activo__vigente=True)

        if especie_filter:
            queryset = queryset.filter(especie__icontains=especie_filter)
        if not hora_filter:
            queryset = queryset.exclude(Q(hora='') | Q(hora='nan'))

        filtered_queryset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
        ).qs

        table = self.table_class(filtered_queryset, order_by="especie")
        RequestConfig(self.request, paginate=True).configure(table)

        context['filter'] = self.filterset_class(
            self.request.GET,
            queryset=queryset,
        )

        especies = queryset
        user = self.request.user

        if user.is_authenticated:
            watchlists = Watchlist.objects.filter(user=user)
            # Diccionario con el estado de la estrella para cada especie
            estrellas_dict = {}
            # Verificar si cada especie está en alguna de las watchlists del usuario
            for especie in especies:
                en_watchlist = watchlists.filter(especies=especie).exists()
                estrellas_dict[especie.id] = en_watchlist
        else:
            # Usuario no autenticado, diccionario = empty
            estrellas_dict = {}

        context['estrellas_dict'] = estrellas_dict
        context['table'] = table
        context['watchlists'] = watchlists if user.is_authenticated else None
        return context
    

class NuevaEspecieView(LoginRequiredMixin, CreateView):
    model = Especie
    form_class = NuevaEspecieForm
    template_name = "nueva_especie.html"
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = get_object_or_404(Tipo, pk=self.kwargs['pk'])
        context['tipo'] = tipo
        context['especies'] = tipo.especies.all()
        return context

    def form_valid(self, form):
        tipo = get_object_or_404(Tipo, pk=self.kwargs['pk'])
        especie = form.save(commit=False)
        especie.tipo = tipo
        especie.save()
        return redirect("especies", pk=tipo.pk)


class EspeciesUsaView(SingleTableView, FilterView):
    model = Especie_USA
    table_class = EspeciesUsaTable
    template_name = "especies_usa.html"
    #paginator_class = LazyPaginator
    #paginate_by = 50
    filterset_class = EspecieFilter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        especie_filter = self.request.GET.get('especie')
        queryset = Especie_USA.objects.all()

        if especie_filter:
            queryset = queryset.filter(especie__icontains=especie_filter)

        filtered_queryset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
        ).qs

        table = self.table_class(filtered_queryset, order_by="especie")
        RequestConfig(self.request, paginate=True).configure(table)
        
        context['filter'] = self.filterset_class(
            self.request.GET,
            queryset=queryset,
        )
        context['table'] = table
        return context
    

def comparador_cedears(request):

    activos = Activo.objects.filter(
        tipo__tipo="CEDEARS",
        ticker_ars__isnull=False,
        ticker_usa__isnull=False,
    ).exclude(ticker_usa__exact="")

    # Obtener el valor del filtro de especie ingresado en el formulario
    especie_filter = request.GET.get('especie', None)

    if especie_filter:
        # Aplicar el filtro de especie en la consulta de la base de datos
        activos = activos.filter(ticker_ars__icontains=especie_filter)

    tabla_filas = []

    for activo in activos:
        especie_ars = Especie.objects.filter(especie=activo.ticker_ars, plazo='48hs').first()
        especie_mep = Especie.objects.filter(especie=activo.ticker_mep, plazo='48hs').first()
        especie_usa = Especie_USA.objects.filter(especie=activo.ticker_usa).first()
        especie_gd30 = Especie.objects.filter(especie='GD30', plazo='48hs').first()
        especie_gd30d = Especie.objects.filter(especie='GD30D', plazo='48hs').first()
        cotiz_mep = especie_gd30.ultimo / especie_gd30d.ultimo if especie_gd30 is not None and especie_gd30d is not None else None
        ratio = activo.ratio

        precio_ars = especie_ars.ultimo if especie_ars and especie_ars.ultimo != 0 else especie_ars.punta_venta if especie_ars and especie_ars.punta_venta != 0 else None
        precio_ars_mep = especie_ars.ultimo / cotiz_mep if especie_ars and especie_ars.ultimo != 0 and cotiz_mep else especie_ars.punta_venta / cotiz_mep if especie_ars and especie_ars.punta_venta != 0 else None
        precio_ars_mep_convertido = precio_ars_mep * ratio if precio_ars_mep else None
        precio_mep = especie_mep.ultimo if especie_mep and especie_mep.ultimo != 0 else especie_mep.punta_venta if especie_mep and especie_mep.punta_venta != 0 else None
        precio_mep_convertido = especie_mep.ultimo * ratio if especie_mep and especie_mep.ultimo != 0 else especie_mep.punta_venta * ratio if especie_mep and especie_mep.punta_venta != 0 else None
        precio_usa = especie_usa.ultimo if especie_usa and especie_usa.ultimo != 0 else especie_usa.punta_venta if especie_usa and especie_usa.punta_venta != 0 else None
        ars_vs_usa = ((precio_ars_mep_convertido / precio_usa - 1) * 100) if precio_ars_mep_convertido is not None and precio_usa is not None else None
        mep_vs_usa = ((precio_mep_convertido / precio_usa - 1) * 100) if precio_mep_convertido is not None and precio_usa is not None else None

        fila = {
            'ticker_ars': activo.ticker_ars,
            'ratio': ratio,
            'precio_ars': precio_ars,
            'precio_ars_mep': precio_ars_mep,
            'precio_ars_mep_convertido': precio_ars_mep_convertido,
            'ticker_mep': activo.ticker_mep,
            'precio_mep': precio_mep,
            'precio_mep_convertido': precio_mep_convertido,
            'ticker_usa': activo.ticker_usa,
            'precio_usa': precio_usa,
            'ars_vs_usa': ars_vs_usa,
            'mep_vs_usa': mep_vs_usa,
            'monto_operado': especie_ars.monto / 1000000 if especie_ars.monto else None
        }

        tabla_filas.append(fila)

    table = ComparadorTable(tabla_filas, order_by="-monto_operado")
    
    context = {
        "table": table,
        "filter": especie_filter,
    }

    RequestConfig(request, paginate=True).configure(table)
    return render(request, "comparador_cedears.html", context)

    
@login_required
def display_watchlists(request):
    watchlists = Watchlist.objects.filter(user=request.user)

    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist = form.save(commit=False)
            watchlist.user = request.user
            watchlist.nombre = form.cleaned_data.get("nombre")
            watchlist.save()
            return redirect(request.path_info)
    else:
        form = WatchlistForm()

    watchlist_tables = {}
    for watchlist in watchlists:
        especies = watchlist.especies.all()
        table = EspeciesTable(especies)
        watchlist_tables[watchlist] = table

    context = {
        'watchlists': watchlists,
        'form': form,
        'watchlist_tables': watchlist_tables,
    }

    return render(request, 'watchlists.html', context)

@login_required
def edit_watchlist(request, watchlist_id):
    watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)

    if request.method == 'POST':
        form = WatchlistForm(request.POST, instance=watchlist)
        if form.is_valid():
            watchlist.nombre = form.cleaned_data.get("nombre")
            form.save()
            return redirect('watchlists')
    else:
        form = WatchlistForm(instance=watchlist)

    context = {
        'form': form,
        'watchlist': watchlist,
    }

    return render(request, 'watchlists.html', context)

@login_required
def delete_watchlist(request, watchlist_id):
    watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)

    if request.method == 'POST':
        watchlist.delete()
        return redirect('watchlists')

    context = {
        'watchlist': watchlist,
    }

    return render(request, 'watchlists.html', context)

@login_required
def add_favorito(request):
    if request.method == 'POST':
        especie_id = request.POST.get('especie_id')
        watchlist_id = request.POST.get('watchlist')

        especie = get_object_or_404(Especie, id=especie_id)
        watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
        watchlist.especies.add(especie)
        watchlist.save()

    return redirect('watchlists')

@login_required
def delete_favorito(request):
    if request.method == 'POST':
        especie_id = request.POST.get('especie_id')
        watchlist_id = request.POST.get('watchlist')

        especie = get_object_or_404(Especie, id=especie_id)
        watchlist = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
        watchlist.especies.remove(especie)
        watchlist.save()

    return redirect('watchlists')

@login_required
def get_watchlists_data(request):
    if request.user.is_authenticated:
        watchlists = Watchlist.objects.filter(user=request.user)
        watchlists_data = [
            {
                "id": watchlist.id,
                "nombre": watchlist.nombre,
                # Aquí puedes incluir la lista de especies que están en la watchlist
                "especies": [especie.id for especie in watchlist.especies.all()]
            }
            for watchlist in watchlists
        ]
        return JsonResponse(watchlists_data, safe=False)
    else:
        return JsonResponse([], safe=False)
    

@csrf_exempt
def store_nasdaq_data(request):
    if request.method == 'POST':
        client_token = request.META.get('HTTP_X_CSRFTOKEN')
        print(request.headers)
        print(client_token)
        if client_token == NASDAQ_DATA_TOKEN:
            data = json.loads(request.body.decode('utf-8'))
            nasdaq_data, created = Nasdaq_Data.objects.get_or_create(pk=1)
            nasdaq_data.json_data = data
            nasdaq_data.save()
            import_to_database_usa(data)
            return JsonResponse({'message': 'JSON guardado y USA actualizado correctamente'})
        else:
            return JsonResponse({'message': 'Token no válido'}, status=403)
    else:
        data = {"message": "Esta es una respuesta de prueba para una solicitud GET."}
        return JsonResponse(data)

