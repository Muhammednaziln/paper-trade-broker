from django import forms

from apps.broking.orders.models import Order


class OrderStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('order_status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_status'].choices = ((stat, stat) for stat in Order.ORDER_PIPELINE[self.instance.order_status])

    def clean_order_status(self):
        old_status = self.instance.order_status
        new_status = self.cleaned_data['order_status']
        if new_status not in Order.ORDER_PIPELINE[old_status]:
            raise forms.ValidationError(f"Order is in the state {old_status} cannot be marked as {new_status}")
        return new_status


