from enum import Enum


class OrderStatus(Enum):
    awaiting_payment = 0
    awaiting_fulfillment = 1
    awaiting_shipment = 2
    delivered = 3
    closed = 4
    cancelled = 5
