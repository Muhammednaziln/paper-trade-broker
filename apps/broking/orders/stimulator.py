

class Stimulator(object):

    def __init__(self, order, constants):
        self.order = order
        self.constants = constants

    def stimulate__accept_order_by_broker(self):
        self.order.set_status(self.constants.OPEN)

    def stimulate__place_order_at_exchange(self):
        self.order.set_status(self.constants.EXECUTED)

    def stimulate__accept_order_by_exchange(self):
        self.order.set_status(self.constants.EXECUTED)

    def stimulate__reject_order_by_exchange(self, reason):
        self.order.set_status()

    def stimulate__cancel_order(self, reason):
        pass