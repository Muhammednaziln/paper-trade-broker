import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    all common users will be traders; users will be is_superuser=True will be super admins.
    """
    fund_balance = models.FloatField(default=0.0)   # actually a cached field computed from apps.broking.funds.TransactionLedger
    date_of_birth = models.DateField(help_text="This can be asked as security question.", null=True)

    def recalculate(self):
        from apps.broking.funds.models import TransactionLedger
        transactions = TransactionLedger.objects.filter(user=self)
        balance = 0.0
        for transaction in transactions:
            if transaction.transaction_type == 'PAY-OUT' or transaction.transaction_type == 'TRADE-SELL':
                balance -= transaction.amount
            else:
                balance += transaction.amount
        self.fund_balance = balance
        self.save()


class TradeApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_name = models.CharField(max_length=32, default='App')
    access_key = models.CharField(max_length=24)
    access_secret = models.CharField(max_length=24)
    redirect_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(24)).decode()

    def save(self, **kwargs):
        if not self.access_key:
            self.access_key = "pt_" + TradeApp.generate_key()
            self.access_secret = "pt_scrt_" + TradeApp.generate_key()
        super().save(**kwargs)



