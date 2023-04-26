from django.urls import path, include

from apps.broking.orders.views.order_creation import (OrderCreateView, OrderDetailView)
from apps.broking.orders.views.trade import OrderListAjaxView, OrderListView


urlpatterns = [
    path('', include([
        path('', OrderListView.as_view(), name="orders_list"),
        path('load-more/', OrderListAjaxView.as_view(), name='order-list-ajax'),

        path('place/', OrderCreateView.as_view(), name="place_order"),
        path('<int:pk>/summarize', OrderDetailView.as_view(), name="orders_detail"),

    ]))
]
