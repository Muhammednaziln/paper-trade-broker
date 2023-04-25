from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.users.models import TradeApp


class TradeAppListView(LoginRequiredMixin, ListView):
    model = TradeApp
    template_name = 'users/trade_app_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TradeAppCreateUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TradeApp
    fields = ('application_name', 'redirect_url')

    template_name = 'users/trade_app_form.html'
    success_url = reverse_lazy('trade-app-list')
    success_message = "The app has been saved"

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset=queryset)
        return None     # for create

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):

        form.save(commit=False)
        form.instance.user = self.request.user
        return super().form_valid(form)


class TradeAppDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TradeApp
    template_name = 'users/trade_app_confirm_delete.html'
    success_url = reverse_lazy('trade-app-list')
    success_message = "The app has been removed"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
