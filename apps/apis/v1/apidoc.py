from collections import OrderedDict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view()
def root(request):
    _url = lambda path, *args, **kwargs: request.build_absolute_uri(reverse(path, args=args, kwargs=kwargs))
    return Response(OrderedDict([
        ("accounts", OrderedDict([
            # ("login", "login--api"),              # sharing access token directly.
            ("profile", _url("profile--api")),
            ("funds", _url("funds--api")),
            ("portfolio", _url("portfolio--api")),
        ])),
        ("orders", OrderedDict([
            ("orders", _url("orders--api")),
            ("order-detail", _url("order-detail--api", broker_id="broker_id")),
            ("place-order", _url("place-order--api")),
            ("cancel-order", _url("cancel-order--api", broker_id="broker_id")),
        ])),
    ]))




