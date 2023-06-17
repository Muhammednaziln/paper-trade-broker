import binascii
import os
from typing import List, Tuple

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.broking.exceptions import OrderStatusPipelineException
from apps.utilities.trade import ltp


class OrderConstants:
    NSE = 'NSE'
    BSE = 'BSE'
    EQUITY = 'EQUITY'
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    SL = 'SL'
    SLM = 'SLM'
    CNC = 'CNC'
    MIS = 'MIS'
    NRML = 'NRML'
    BUY = 'BUY'
    SELL = 'SELL'
    DAY = 'DAY'
    IOC = 'IOC'
    PROCESSING = 'PROCESSING'
    OPEN = 'OPEN'
    EXECUTED = 'EXECUTED'
    REJECTED_BY_BROKER = 'REJECTED_BY_BROKER'
    REJECTED_BY_EXCHANGE = 'REJECTED_BY_EXCHANGE'
    CANCELLED = 'CANCELLED'


class Order(models.Model):

    SYMBOL_CHOICES = [
        ('NSE', 'NSE'),
        ('BSE', 'BSE'),
    ]
    EXCHANGE_TYPE_CHOICES = [
        ('EQUITY', 'Equity'),
    ]
    ORDER_TYPE_CHOICES = [
        ('LIMIT', 'Limit'),
        ('MARKET', 'Market'),
        ('SL', 'SL'),
        ('SLM', 'SLM'),
    ]
    PRODUCT_TYPE_CHOICES = [
        ('CNC', 'CNC'),
        ('MIS', 'Intraday'),
        ('NRML', 'Normal'),
    ]
    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    VALIDITY_CHOICES: list[tuple[str, str]] = [
        ('DAY', 'Day'),
        ('IOC', 'IOC'),
    ]

    ORDER_STATUS_CHOICES: list[tuple[str, str]] = [
        ('PROCESSING', 'PROCESSING AT BROKER / AMO'),
        ('OPEN', 'OPEN AT MARKET / AWAITING EXECUTION'),
        ('EXECUTED', 'EXECUTED IN MARKET'),
        ('REJECTED_BY_BROKER', 'REJECTED BY BROKER'),
        ('REJECTED_BY_EXCHANGE', 'REJECTED BY EXCHANGE'),
        ('CANCELLED', 'CANCELLED BY USER'),
    ]

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(25)).decode().upper()

    # ORDER DETAILS
    symbol = models.ForeignKey('broking.Symbol', on_delete=models.CASCADE)
    exchange = models.CharField(max_length=10, choices=SYMBOL_CHOICES)
    exchange_type = models.CharField(max_length=10, choices=EXCHANGE_TYPE_CHOICES, blank=True, null=True)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    validity = models.CharField(max_length=10, choices=VALIDITY_CHOICES)

    quantity = models.IntegerField()
    limit_price = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    trigger_price = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    stop_loss_price = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    is_amo = models.BooleanField(default=False)
    algo_id = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="(Optional) If User have any algo id for ref.")

    # META DETAILS
    order_placed_at = models.DateTimeField(auto_now_add=True)
    order_placed_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    trade_app = models.ForeignKey('users.TradeApp', on_delete=models.CASCADE, null=True, blank=True)
    basket_code = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="User can create a unique basket id and sent the same for multiple orders.")

    # BROKER ADJUSTMENTS
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, default="PROCESSING", max_length=20)
    broker_error_message = models.DateTimeField(auto_now_add=True)
    broker_id = models.CharField(max_length=25, blank=True, null=True)

    # EXCHANGE ADJUSTMENTS
    exchange_error_message = models.DateTimeField(auto_now_add=True)
    exchange_id = models.CharField(max_length=25, blank=True, null=True)
    filled_quantity = models.IntegerField(default=0)
    amount = models.IntegerField(null=True, blank=True)

    ORDER_PIPELINE = {
        'PROCESSING': ('OPEN', 'REJECTED_BY_BROKER', 'CANCELLED'),
        'OPEN': ('EXECUTED', 'REJECTED_BY_BROKER', 'REJECTED_BY_EXCHANGE', 'CANCELLED'),
        'EXECUTED': (),
        'CANCELLED': (),
        'REJECTED_BY_EXCHANGE': (),
        'REJECTED_BY_BROKER': (),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.broking.orders.stimulator import Stimulator
        self.stimulator = Stimulator(self, OrderConstants)

    def set_status(self, new_status):
        old_status = self.order_status
        if new_status not in Order.ORDER_PIPELINE[old_status]:
            raise OrderStatusPipelineException(old_status, new_status, self)
        self.order_status = new_status
        OrderStatus.objects.create(order=self, old_status=old_status, new_status=new_status)
        if new_status == OrderConstants.EXECUTED:
            self._trigger_exchange_executed()
        elif new_status == OrderConstants.REJECTED_BY_EXCHANGE:
            self._trigger_exchange_rejected()
        self.save()

    @property
    def has_next_status(self):
        return bool(self.ORDER_PIPELINE[self.order_status])

    def _trigger_exchange_executed(self, filled_quantity=0):
        from apps.broking.stock_exchange.models import ExchangeTransaction, DematAccountEntry
        from apps.broking.funds.models import TransactionLedger

        if self.ORDER_TYPE_CHOICES in [OrderConstants.LIMIT, OrderConstants.SL]:
            amount = self.limit_price
        else:
            maps = ltp(self.symbol.symbol)
            amount = maps[self.symbol.symbol]
        self.amount = amount * self.quantity
        self.filled_quantity = self.quantity             # TODO : Add partial quantity trigger.
        if self.exchange_id is None:
            self.exchange_id = Order.generate_key()

        tl = TransactionLedger(
            amount=amount,
            user=self.order_placed_by,
            reference=self.exchange_id,
        )

        account = DematAccountEntry.get_account_from_order(self)
        et = ExchangeTransaction(
            account=account,
            order=self,
            quantity=self.quantity,
            amount=amount
        )
        et.save()           # to trigger save signal.

    def _trigger_exchange_rejected(self):
        if self.exchange_id is None:
            self.exchange_id = Order.generate_key()

    def save(self, **kwargs):
        if self.broker_id is None:
            self.broker_id = Order.generate_key()
        super().save(**kwargs)

    @property
    def ordered_via(self):
        return ('API', 'DASHBOARD')[not self.trade_app_id]

    def validate_order_input(self):
        return


class OrderStatus(models.Model):

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Order)
def order_validation(instance: Order, **kwargs):
    instance.validate_order_input()



