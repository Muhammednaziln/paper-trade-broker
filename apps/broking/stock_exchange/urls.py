from django.urls import path, include

from apps.broking.stock_exchange.views import MyPortfolioView

urlpatterns = [
    # path('', function, name="index")
    path('', MyPortfolioView.as_view(), name="portfolio"),
]
