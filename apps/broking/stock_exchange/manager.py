from django.db import models


class ExchangeTransactionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def buy_transactions(self):
        return self.get_queryset().filter(order__transaction_type='SELL')

    def symbol(self, symbol):
        return self.get_queryset().filter(symbol=symbol)

    def sell_transactions(self):
        return self.get_queryset().filter(order__transaction_type='BUY')

    def intraday_orders(self):
        return self.get_queryset().filter(order__product_type='MIS')

    def delivery_orders(self):
        return self.get_queryset().exclude(order__product_type='MIS')

