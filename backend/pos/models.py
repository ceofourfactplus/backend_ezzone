
from collections import defaultdict
from django.db import models
from customer.models import AddressCustomer
from promotion.models import PromotionPackage, Voucher, PointPromotion
from product.models import SaleChannel, Product, Topping
from backend.settings import AUTH_USER_MODEL
from customer.models import Customer
from consignment.models import ConsignmentProduct

from django.utils.translation import gettext_lazy as _


def upload_to_payment(instance, filename):
    return 'payment/{filename}'.format(filename=filename)


class Payment(models.Model):
    img = models.ImageField(
        _("Image"), upload_to=upload_to_payment, null=True, default=None)
    payment = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    descriptions = models.TextField(null=True, blank=True, default='')


class Order(models.Model):
    DELIVERY = 1
    EATHERE = 0
    STATUS_DELIVERY = (
        (DELIVERY, 'delivery'),
        (EATHERE, 'eat_here')
    )

    WAITING = 0
    ON_COOKING = 1
    ON_DELIVERY = 2
    FINISH = 3
    VOID = 4
    STATUS_ORDER = (
        (WAITING, 'waiting'),
        (ON_COOKING, 'on cooking'),
        (ON_DELIVERY, 'on delivery'),
        (FINISH, 'finish'),
        (VOID, 'void')
    )

    WAITING_ORDER = 0
    ON_COOKING_ORDER = 1
    ON_SERVE = 2
    FINISH_ORDER = 3
    STATUS_ORDER_DETAIL = (
        (WAITING_ORDER, 'waiting'),
        (ON_COOKING_ORDER, 'on cooking'),
        (ON_SERVE, 'on serve'),
        (FINISH_ORDER, 'finish'),
    )

    COD = 1
    CREDIT = 2
    CASH = 3
    TRANSFER = 4
    STATUS_PAYMENT = (
        (COD, 'cash on delivery'),
        (CREDIT, 'credit'),
        (CASH, 'cash'),
        (TRANSFER, 'transfer')
    )
    order_number = models.CharField(max_length=20, default='1')
    total_balance = models.DecimalField(max_digits=7, decimal_places=2)
    table = models.IntegerField(null=True, default=None)
    discount_percent = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)
    address = models.ForeignKey(
        AddressCustomer, on_delete=models.PROTECT, default=None, null=True)
    status_delivery = models.IntegerField(choices=STATUS_DELIVERY)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_amount = models.IntegerField()
    payment_status = models.IntegerField(
        choices=STATUS_PAYMENT, default=TRANSFER)
    payment = models.ForeignKey(
        Payment, on_delete=models.PROTECT, null=True, default=None)
    sale_channel = models.ForeignKey(SaleChannel, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    delivery_price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField(null=True, blank=True, default='')
    status_order = models.IntegerField(
        choices=STATUS_ORDER, default=WAITING)
    status_drink = models.IntegerField(
        choices=STATUS_ORDER_DETAIL, null=True, default=None)
    status_food = models.IntegerField(
        choices=STATUS_ORDER_DETAIL, null=True, default=None)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="order_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="order_update_by", null=True, blank=True, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True, default=None)
    voucher = models.ForeignKey(
        Voucher, on_delete=models.PROTECT, null=True, blank=True, default=None)
    point_promotion = models.ForeignKey(
        PointPromotion, on_delete=models.PROTECT, null=True, blank=True, default=None)
    point = models.IntegerField(null=True, blank=True, default=None)
    cash = models.IntegerField(null=True, default=None)
    change = models.IntegerField(null=True, default=None)
    spen_time = models.TimeField(null=True, default=None)
    reason = models.TextField(blank=True, default='')


class OrderItem(models.Model):
    FLAVOUR_0 = 0
    FLAVOUR_50 = 1
    FLAVOUR_100 = 2
    FLAVOUR_150 = 3
    FLAVOUR_LEVEL = (
        (FLAVOUR_0, 'none'),
        (FLAVOUR_50, 'low'),
        (FLAVOUR_100, 'medium'),
        (FLAVOUR_150, 'very')
    )

    SIZE_S = 'S'
    SIZE_M = 'M'
    SIZE_L = 'L'
    SIZE = (
        (SIZE_S, 'S'),
        (SIZE_M, 'M'),
        (SIZE_L, 'L')
    )

    WAITING_ORDER = 0
    ON_COOKING_ORDER = 1
    ON_SERVE = 2
    FINISH_ORDER = 3
    STATUS_ORDER = (
        (WAITING_ORDER, 'waiting'),
        (ON_COOKING_ORDER, 'on cooking'),
        (ON_SERVE, 'on serve'),
        (FINISH_ORDER, 'finish'),
    )
    status_order = models.IntegerField(
        choices=STATUS_ORDER, default=WAITING_ORDER)
    code = models.CharField(max_length=100)
    flavour_level = models.IntegerField(choices=FLAVOUR_LEVEL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, null=True, default=None)
    topping = models.ForeignKey(
        Topping, on_delete=models.PROTECT, null=True, default=None)
    consignment = models.ForeignKey(
        ConsignmentProduct, on_delete=models.PROTECT, null=True, default=None)
    package = models.ForeignKey(
        PromotionPackage, on_delete=models.PROTECT, null=True, default=None)
    price_item = models.DecimalField(max_digits=7, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=SIZE, default=SIZE_M)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(null=True)
    amount = models.IntegerField()
    item_in_package = models.BooleanField(default=False)


class OrderItemTopping(models.Model):
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.PROTECT)
    price_topping = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    amount = models.IntegerField()
