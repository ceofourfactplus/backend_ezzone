from django.db import models
from django.utils.translation import gettext_lazy as _
from backend.settings import AUTH_USER_MODEL
from product.models import SaleChannel
from raw_material.models import Unit


def upload_to_consignment(instance, filename):
    return 'consignment/{filename}'.format(filename=instance.name)


class Consigner(models.Model):
  nick_name = models.CharField(max_length=40)
  first_name = models.CharField(max_length=40)
  last_name = models.CharField(max_length=40)
  line_id = models.CharField(max_length=40)
  phone_number = models.CharField(max_length=13)
  address = models.TextField()
  email = models.EmailField()
  id_card = models.CharField(max_length=13)
  birth_date = models.DateField()
  cradit_cart = models.CharField(max_length=13)
  

class ConsignmentProduct(models.Model):
    OUT_OF_STOCK = 0
    ALMOST_OUT_OF_STOCK = 1
    INSTOCK = 2
    STATUS_STOCK = (
        (OUT_OF_STOCK, 'สินค้าหมด'),
        (ALMOST_OUT_OF_STOCK, 'สินค้าเกือบหมด'),
        (INSTOCK, 'สินค้าพร้อมขาย')
    )

    old_product = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, default=None)
    img = models.ImageField(
        _("Image"), upload_to=upload_to_consignment, default=None, null=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    status = models.IntegerField(default=INSTOCK, choices=STATUS_STOCK)
    remain = models.IntegerField(default=0)
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=None, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    consignment = models.ForeignKey(
        Consigner, on_delete=models.PROTECT, null=True, default=None)
    share = models.IntegerField(default=0)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="consignment_product_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="consignment_product_update_by", 
        null=True, blank=True, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True, default=None)

class AddConsignment(models.Model):
    consignment = models.ForeignKey(ConsignmentProduct,on_delete=models.PROTECT)
    amount = models.IntegerField()
    create_by = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT, related_name="add_consignment_create_by")
    create_at = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT,null=True,default=None, related_name="add_consignment_update_by")

class PriceConsignment(models.Model):
    price = models.DecimalField(max_digits=6,decimal_places=2)
    consignment = models.ForeignKey(ConsignmentProduct,on_delete=models.CASCADE)
    sale_channel = models.ForeignKey(SaleChannel,on_delete=models.CASCADE)

class ConsignmentPayment(models.Model):
    payment = models.IntegerField()
    price = models.DecimalField
    consignment = models.ForeignKey(ConsignmentProduct,on_delete=models.PROTECT)
