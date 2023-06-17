from django.shortcuts import render
from django.urls import path, include

from apps.apis.v1.apidoc import root
from apps.apis.v1.views import (
    Portfolio, fund_balance, get_profile, OrderListAPIView, OrderCreateView, OrderRetrieveView, cancel_order
)

urlpatterns = [
    path('', root, name="root"),
    path('accounts/', include([
        path('profile', get_profile, name="profile--api"),
        path('funds', fund_balance, name="funds--api"),
        path('portfolio', Portfolio.as_view(), name="portfolio--api"),
    ])),
    path('orders/', include([
        path('', OrderListAPIView.as_view(), name="orders--api"),
        path('place/', OrderCreateView.as_view(), name="place-order--api"),
        path('<str:broker_id>/detail/', OrderRetrieveView.as_view(), name="order-detail--api"),
        path('<str:broker_id>/cancel/', cancel_order, name="cancel-order--api"),
    ])),

]


