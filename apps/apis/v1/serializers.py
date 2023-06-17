from rest_framework import serializers
from apps.broking.orders.models import Order
from apps.broking.stock_exchange.models import DematAccountEntry


class DematAccountEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DematAccountEntry
        fields = ['symbol', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_updates = serializers.SerializerMethodField()

    def get_order_updates(self, instance):
        return [{
            'old_status': s.old_status,
            'new_status': s.new_status,
            'created_at': s.created_at,
        } for s in instance.order_status_set.all().order_by('id')]

    class Meta:
        model = Order
        fields = [
            'symbol', 'exchange', 'exchange_type', 'order_type', 'product_type', 'transaction_type', 'validity',
            'quantity', 'limit_price', 'trigger_price', 'stop_loss_price', 'is_amo', 'algo_id', 'basket_code'
            'order_placed_at', 'trade_app', 'order_status', 'broker_error_message', 'broker_id',
            'exchange_error_message', 'exchange_id', 'filled_quantity', 'amount', 'order_updates',
        ]

        read_only_fields = [
            'order_placed_at', 'trade_app', 'order_status', 'broker_error_message', 'broker_id',
            'exchange_error_message', 'exchange_id', 'filled_quantity', 'amount', 'order_updates'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    symbol = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['symbol', 'basket_id', 'order_status', 'exchange', 'order_type', 'transaction_type', 'algo_id', 'basket_code',
                  'basket_code', 'quantity', 'filled_quantity', 'broker_error_message', 'exchange_error_message',
                  'exchange_id', 'amount']


