from enum import Enum


class OrderStatus(str, Enum):
    awaiting_payment = 'awaiting_payment'
    awaiting_fulfillment = 'awaiting_fulfillment'
    awaiting_shipment = 'awaiting_shipment'
    delivered = 'delivered'
    closed = 'closed'
    cancelled = 'cancelled'
