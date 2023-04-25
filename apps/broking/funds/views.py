import binascii
import os

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TransactionLedger


class PayInList(LoginRequiredMixin, View):
    def get(self, request):
        payins = TransactionLedger.objects.filter(user=request.user, transaction_type='PAY-IN')
        return render(request, 'funds/payin_list.html', {'payins': payins})


def generate_reference():
    return "TXN" + binascii.hexlify(os.urandom(12)).decode().upper()


class PayInCreate(LoginRequiredMixin, View):

    def get(self, request):
        reference = generate_reference()  # function to generate unique reference
        description = 'Account recharge'
        return render(request, 'funds/payin_create.html', {'reference': reference, 'description': description})

    def post(self, request):
        amount = request.POST.get('amount')
        reference = request.POST.get('reference')
        description = request.POST.get('description')
        TransactionLedger.objects.create(amount=amount, user=request.user, description=description, reference=reference,
                                         transaction_type='PAY-IN')
        update_fund_balance(request.user)
        messages.success(request, 'PAY-IN transaction created successfully.')
        return redirect('payin_list')


def update_fund_balance(user):
    transactions = TransactionLedger.objects.filter(user=user)
    balance = 0.0
    for transaction in transactions:
        if transaction.transaction_type == 'PAY-OUT' or transaction.transaction_type == 'TRADE-SELL':
            balance -= transaction.amount
        else:
            balance += transaction.amount
    user.fund_balance = balance
    user.save()