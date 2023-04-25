from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from apps.broking.stock_exchange.manager import ExchangeTransactionManager


class DematAccountEntry(models.Model):
    """
    This model represents a user's entry in their Demat account.
    Note that in this implementation, we named the model 'DematAccountStock' assuming that the user instance itself
    acts as both the Demat account and payment account.

    However, this overfills functionalities, and it is not considered a good approach.
    Ideally, a user account should have a Demat account and a separate payment account.

    Therefore, on ideal case, instead of pointing to the user, `DematAccountEntry` should be pointed to the Demat
    account, similar to the case of the payment account. This way, the Demat account can be updated independently
    of the user account, which is more scalable and maintainable.

    Right now this is expected to ba a contribution, not to getting overfeed over micro functionality,
    but to complete the project.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    symbol = models.ForeignKey('broking.Symbol', on_delete=models.CASCADE)
    quantity = models.IntegerField(help_text="Summary of net Quantity of net transaction.")

    @classmethod
    def get_account_from_order(cls, order):
        account = None
        try:
            account, _ = cls.objects.get_or_create(user=order.order_placed_by, symbol=order.symbol)
        except MultipleObjectsReturned:
            # There is no way to happen this. still if data got manipulated, We have to handle.
            # Code complexity is not considered as this is a rare situation.
            extra_objects = cls.objects.filter(user=order.order_placed_by, symbol=order.symbol).order_by('id').values_list('id', flat=True)[1:]
            cls.objects.filter(id__in=extra_objects).delete()
            account = cls.objects.get(user=order.order_placed_by, symbol=order.symbol)
        account.recalculate()

    def recalculate(self):
        self.quantity = self.transactions.all().symbol(self.symbol).aggregate(
            quantity=models.Sum('quantity')
        )['quantity'] or 0
        self.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'symbol'], name='unique_user_symbol_for_demat'),
        ]


class ExchangeTransaction(models.Model):
    account = models.ForeignKey(DematAccountEntry, on_delete=models.CASCADE, related_name='transactions', verbose_name="Transfer To Account")
    order = models.ForeignKey('broking.Symbol', on_delete=models.CASCADE)
    quantity = models.IntegerField(help_text="Storing quantity as negative if its a 'SELL' order other vice store as positive.")
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ExchangeTransactionManager()

