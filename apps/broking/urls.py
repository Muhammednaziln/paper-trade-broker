from django.urls import path, include

from apps.broking.views import SymbolListView

urlpatterns = [
    path('symbols/', SymbolListView.as_view(), name='symbol_list'),
]
