

class OrderStatusPipelineException(Exception):
    message = "You cannot update order status from {old_status} to {new_status}. #ORD{order_id}"

    def __init__(self, old_status, new_status, order):
        self.message = self.message.format(old_status=old_status, new_status=new_status, order_id=order.id)
