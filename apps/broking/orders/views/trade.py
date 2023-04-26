from django.views.generic import ListView, TemplateView
from apps.broking.orders.models import Order


class OrderListView(TemplateView):
    template_name = 'orders/orders_list.html'

    def get_context_data(self, **kwargs):
        orders = Order.objects.order_by('order_status', '-id').all()
        status_list = Order.ORDER_STATUS_CHOICES
        status_pills = []
        for status in status_list:
            status_orders = orders.filter(order_status=status[0])
            status_pills.append({
                'status_name': status[1],
                'status_slug': status[0],
                'status_count': status_orders.count(),
                'status_orders': status_orders[:10],
            })

        context = {
            'status_pills': status_pills,
            'recent_transactions': orders[:5],
        }
        return super().get_context_data(**context)


class OrderListAjaxView(ListView):
    model = Order
    template_name = 'orders/orders_list_ajax.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('order_status', '-id')
        status = self.request.GET.get('status', None)
        if status:
            queryset = queryset.filter(order_status=status)
        return queryset

