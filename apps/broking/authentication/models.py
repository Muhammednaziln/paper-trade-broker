import binascii
import os

from django.db import models
from django.utils.datetime_safe import datetime


class AuthSession(models.Model):
    app = models.ForeignKey('users.TradeApp', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=18)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(18)).decode()

    def save(self, **kwargs):
        if not self.access_token:
            self.access_token = AuthSession.generate_key()
        return super().save(**kwargs)

    # used to check logout before expiry time. after expiry this flag do not have any validity even if it's true.
    @property
    def expires_at(self):
        if self.created_at:
            return datetime(
                year=self.created_at.year,
                month=self.created_at.month,
                day=self.created_at.day,
                hour=23, minute=59, second=59
            )

