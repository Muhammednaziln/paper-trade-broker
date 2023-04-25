from django.db import models


class TransactionLedger(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    reference = models.CharField(max_length=40)
    transaction_type = models.CharField(max_length=20, choices=[
            ('PAY-IN', 'Account Recharge'),
            ('PAY-OUT', 'Payment to Bank Account'),
            ('TRADE-SELL', 'Income from Selling Securities'),
            ('TRADE-BUY', 'Outflow while Buying Securities'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)




