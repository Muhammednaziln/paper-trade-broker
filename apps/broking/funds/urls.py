from django.urls import path, include

from apps.broking.funds.views import PayInList, PayInCreate

urlpatterns = [
    path('', include([
        path('', PayInList.as_view(), name="payin_list"),
        path('recharge-demat-account/', PayInCreate.as_view(), name="payin_create"),
    ]))
]
