from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from apps.broking.orders.forms import OrderStatusUpdateForm
from apps.broking.orders.models import Order, OrderStatus


class OrderCreateView(SuccessMessageMixin, CreateView):
    model = Order
    fields = [
        'symbol', 'exchange', 'exchange_type', 'order_type', 'product_type', 'transaction_type', 'validity',
        'quantity', 'limit_price', 'trigger_price', 'stop_loss_price', 'is_amo', 'basket_code']
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders_list')
    success_message = "Order has been created."

    def form_valid(self, form):
        form.instance.order_placed_by = self.request.user
        return super().form_valid(form)


class OrderDetailView(UpdateView):
    model = Order
    form_class = OrderStatusUpdateForm
    template_name = 'orders/order_detail.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_queryset(self):
        return self.model.objects.filter(order_placed_by=self.request.user)

    def form_valid(self, form):
        order = form.instance
        order.refresh_from_db(fields=('order_status', ))
        order.set_status(form.cleaned_data['order_status'])
        messages.success(self.request, "Order Status has been updated.")
        return HttpResponseRedirect(reverse('orders_detail', kwargs=self.kwargs))

    def get_context_data(self, **kwargs):
        kwargs['status_changes'] = OrderStatus.objects.filter(order_id=self.kwargs['pk'], order__order_placed_by=self.request.user).order_by('id')
        return super().get_context_data(**kwargs)




