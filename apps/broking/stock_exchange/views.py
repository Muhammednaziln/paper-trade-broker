from django.shortcuts import render

from django.views.generic import ListView
from .models import DematAccountEntry, ExchangeTransaction


class MyPortfolioView(ListView):
    template_name = 'stock_exchange/my_portfolio.html'
    context_object_name = 'shares'
    paginate_by = 30

    def get_queryset(self):
        return DematAccountEntry.objects.filter(user=self.request.user).order_by('-quantity')


