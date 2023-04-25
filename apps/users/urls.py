from django.urls import path, include
from django.views.generic import TemplateView

from apps.users.views import (TradeAppListView, TradeAppCreateUpdateView, TradeAppDeleteView)

urlpatterns = [
    path('', TemplateView.as_view(template_name="layouts/base.html"), name="dashboard"),
    path('trade-app/', include([
        path('', TradeAppListView.as_view(), name="trade-app-list"),
        path('create/', TradeAppCreateUpdateView.as_view(), name="trade-app-create"),
        path('<int:pk>/update/', TradeAppCreateUpdateView.as_view(), name="trade-app-update"),
        path('<int:pk>/delete/', TradeAppDeleteView.as_view(), name="trade-app-delete"),
    ]))
]
