from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.apis.v1.serializers import DematAccountEntrySerializer, OrderSerializer, OrderListSerializer
from apps.broking.exceptions import OrderStatusPipelineException
from apps.broking.orders.models import Order, OrderConstants
from apps.broking.stock_exchange.models import DematAccountEntry
from apps.users.models import User


@api_view()
@permission_classes((IsAuthenticated, ))
def get_profile(request):
    u: User = request.user
    return Response({
        "response": {
            "full_name": u.get_full_name(),
            "fund_balance": u.fund_balance,
            "email": u.email,
        }
    })


@api_view()
@permission_classes((IsAuthenticated, ))
def fund_balance(request):
    u: User = request.user
    return Response({
        "response": {
            "fund_balance": u.fund_balance,
        }
    })


class Portfolio(ListAPIView):
    serializer_class = DematAccountEntrySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = DematAccountEntry.objects.filter(user=self.request.user).exclude(quantity=0).order_by('-quantity')
        return queryset


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
            order_placed_by=self.request.user, trade_app=self.request.trade_app,
            broker_error_message="Order Placed successfully.", broker_id=Order.generate_key()
        )


class OrderRetrieveView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
            order_placed_by=self.request.user, trade_app=self.request.trade_app,
            broker_error_message="Order Placed successfully.", broker_id=Order.generate_key()
        )


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Order.objects.all().filter(order_placed_by=self.request.user).order_by('-id')
        return queryset


@api_view()
@permission_classes(IsAuthenticated,)
def cancel_order(request, broker_id):
    order = Order.objects.all().filter(
        order_placed_by=request.user,
        broker_id=broker_id
    ).last()
    if not order:
        return Response({'message': f'Order with {broker_id} is not available.', 'success': False})
    try:
        order.set_status(OrderConstants.CANCELLED)
    except OrderStatusPipelineException as e:
        return Response({'error': f'Order with {broker_id} cannot be cancelled at this point.', 'success': False})
    return Response({'error': f'Order with {broker_id} has been cancelled', 'success': True})

