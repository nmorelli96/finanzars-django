from django.views.generic import View, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


from django.contrib.auth.models import User
from .models import Tipo, Especie, Especie_USA
from cuentas.models import Watchlist
from .forms import NuevaEspecieForm
from cuentas.forms import WatchlistForm

from django_filters.views import FilterView 
from .tables import EspeciesTable, TiposTable, EspecieFilter, EspeciesUsaTable
from django_tables2 import SingleTableView, RequestConfig


# Create your views here.
class TiposView(SingleTableView):
    ''' class based
    tipos = Tipo.objects.all()
    def render(self, request):
        return render(request, 'tipos.html', {'tipos': self.tipos})
    
    def get(self, request):
        return self.render(request)
        '''

    
    model = Tipo
    table_class = TiposTable
    #success_url = reverse_lazy('tipos')
    template_name = "tipos.html"
    
    
    '''
    function

    tipos = Tipo.objects.all()
    return render(
        request, "tipos.html", {"tipos": tipos}
    )  # en settings ya esta configurado BASE_DIR/templates/'''


def contact(request):
    return render(request, "contact.html")

class EspeciesView(SingleTableView, FilterView):
    model = Especie
    table_class = EspeciesTable
    template_name = "especies.html"
    #paginator_class = LazyPaginator
    #paginate_by = 50
    filterset_class = EspecieFilter
    
    def get_table_data(self):
        tipo = get_object_or_404(Tipo, pk=self.kwargs['pk'])
        return tipo.especies.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = get_object_or_404(Tipo, pk=self.kwargs['pk'])
        queryset = context['tipo'].especies.all()
        plazo_filter = self.request.GET.get('plazo')
        hora_filter = self.request.GET.get('hora')
        especie_filter = self.request.GET.get('especie')

        if especie_filter:
            queryset = queryset.filter(especie__icontains=especie_filter)
        if not plazo_filter:
            queryset = queryset.filter(plazo='48hs')
        if not hora_filter:
            queryset = queryset.exclude(hora='')

        filtered_queryset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
        ).qs

        table = self.table_class(filtered_queryset, order_by="especie")
        RequestConfig(self.request, paginate=True).configure(table)
        
        context['filter'] = self.filterset_class(
            self.request.GET or {'plazo': '48hs'},
            queryset=queryset,
        )

        # Obtener las especies del contexto
        especies = queryset

        # Obtener el usuario autenticado
        user = self.request.user

        if user.is_authenticated:
            # Obtener las watchlists del usuario actual
            watchlists = Watchlist.objects.filter(user=user)

            # Crear un diccionario para almacenar el estado de la estrella para cada especie
            estrellas_dict = {}

            # Verificar si cada especie está en alguna de las watchlists del usuario
            for especie in especies:
                en_watchlist = watchlists.filter(especies=especie).exists()
                estrellas_dict[especie.id] = en_watchlist
        else:
            # Si el usuario no está autenticado, establecer el diccionario como vacío
            estrellas_dict = {}


        # Agregar el diccionario al contexto
        context['estrellas_dict'] = estrellas_dict
        print(estrellas_dict)
        context['table'] = table
        context['watchlists'] = watchlists if user.is_authenticated else None
        return context
    

'''def especies(request, pk):
    tipo = get_object_or_404(Tipo, pk=pk)
    especies = tipo.especies.all()  # type: ignore
    return render(request, "especies.html", {"tipo": tipo, "especies": especies})
'''

'''    def render(self, request, pk):
        tipo = get_object_or_404(Tipo, pk=pk)
        especies = tipo.especies.all()  # type: ignore
        
        return render(request, 'especies.html', {"tipo": tipo, "especies": especies})
    
    def get(self, request, pk):
        return self.render(request, pk)
'''

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


'''@login_required
def nueva_especie(request, pk):
    tipo = get_object_or_404(Tipo, pk=pk)
    especies = tipo.especies.all()  # type: ignore

    if request.method == "POST":
        form = NuevaEspecieForm(request.POST)
        if form.is_valid():
            especie = form.save(commit=False)
            especie.tipo = tipo
            especie.especie = form.cleaned_data.get("especie")
            especie.plazo = form.cleaned_data.get("plazo")
            especie.apertura = form.cleaned_data.get("apertura")
            especie.ultimo = form.cleaned_data.get("ultimo")
            especie.cierre_ant = form.cleaned_data.get("cierre_ant")
            especie.var = form.cleaned_data.get("var")
            especie.hora = form.cleaned_data.get("hora")
            especie.save()

            return redirect("especies", pk=tipo.pk)

    else:
        form = NuevaEspecieForm()

    return render(
        request,
        "nueva_especie.html",
        {"tipo": tipo, "especies": especies, "form": form},
    )
'''

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
