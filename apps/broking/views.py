from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Symbol


class SymbolListView(LoginRequiredMixin, ListView):
    model = Symbol
    template_name = 'broking/symbols_list.html'
    context_object_name = 'symbols'
    paginate_by = 30        # number of symbols to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q')
        if search_term:
            queryset = queryset.filter(Q(symbol__icontains=search_term)|Q(display_name__icontains=search_term))  # filter by symbol name
        return queryset.order_by('symbol')  # sort symbols by name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '')
        return context
