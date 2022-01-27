from django.db import models
from django.db.models.deletion import PROTECT
from backend.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _
from raw_material.models import Unit



def upload_to_product(instance, filename):
    return 'product/{filename}'.format(filename=filename)


def upload_to_topping(instance, filename):
    return 'topping/{filename}'.format(filename=filename)


def upload_to_sale_channel(instance, filename):
    return 'sale_channel/{filename}'.format(filename=filename)


class SaleChannel(models.Model):
    status = models.BooleanField(default=True)
    img = models.ImageField(_("Image"), upload_to=upload_to_sale_channel,null=True,default=None)
    sale_channel = models.CharField(max_length=100)
    gp = models.IntegerField(null=True, blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sale_channel_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sale_channel_update_by", null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True,default=None)
    
    @property
    def pricetopping(self):
        return self.pricetopping_set.all()

    @property
    def priceproduct(self):
        return self.priceproduct_set.all()

# topping
class ToppingCategory(models.Model):
    category = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="topping_category_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="topping_category_update_by", null=True, blank=True)


class Topping(models.Model):
    NONE_PICK_UP = 0
    PRODUCT = 1
    MATERIAL = 2
    WAREHOUSE = (
        (NONE_PICK_UP, 'ไม่ต้องตัดสต็อก'),
        (PRODUCT, 'สินค้าพร้อมขาย'),
        (MATERIAL, 'วัตถุดิบ')
    )

    OUT_OF_STOCK = 0
    ALMOST_OUT_OF_STOCK = 1
    INSTOCK = 2
    STATUS_STOCK = (
        (OUT_OF_STOCK, 'สินค้าหมด'),
        (ALMOST_OUT_OF_STOCK, 'สินค้าเกือบหมด'),
        (INSTOCK, 'สินค้าพร้อมขาย')
    )

    DRESSERT = 1
    DRINK = 2
    FOOD = 3
    TYPE_TOPPING = (
        (FOOD, 'ของคาว'),
        (DRINK, 'ของหวาน'),
        (DRESSERT, 'ขนม'),
    )
    img = models.ImageField(
        _("Image"), upload_to=upload_to_topping, default=None, null=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    status = models.IntegerField(default=INSTOCK, choices=STATUS_STOCK)
    remain = models.IntegerField(default=0)
    type_topping = models.IntegerField(choices=TYPE_TOPPING)
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=None, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    warehouse = models.IntegerField(choices=WAREHOUSE, default=NONE_PICK_UP)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="topping_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="topping_update_by", 
        null=True, blank=True, default=None)
    create_at = models.DateTimeField(auto_now_add=True)

class PriceTopping(models.Model):
    status = models.BooleanField(default=True)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    sale_channel = models.ForeignKey(SaleChannel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.ForeignKey(
        'self', on_delete=models.PROTECT, null=True, blank=True)

class SetTopping(models.Model):
    topping = models.ForeignKey(Topping,on_delete=models.CASCADE)
    category = models.ForeignKey(ToppingCategory,on_delete=models.CASCADE)

class ProductCategory(models.Model):
    DESSERT = 1
    DRINK = 2
    FOOD = 3
    TYPE_CATEGORY = (
        (DESSERT, 'ของหวาน'),
        (DRINK, 'เครื่องดื่ม'),
        (FOOD, 'อาหาร'),
    )

    category = models.CharField(max_length=100)
    type_category = models.IntegerField(choices=TYPE_CATEGORY)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="product_category_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="product_category_update_by", null=True, blank=True)


class Product(models.Model):
    NONE_PICK_UP = 0
    PRODUCT = 1
    MATERIAL = 2
    WAREHOUSE = (
        (NONE_PICK_UP, 'ไม่ต้องตัดสต็อก'),
        (PRODUCT, 'สินค้าพร้อมขาย'),
        (MATERIAL, 'วัตถุดิบ')
    )

    OUT_OF_STOCK = 0
    ALMOST_OUT_OF_STOCK = 1
    INSTOCK = 2
    STATUS_STOCK = (
        (OUT_OF_STOCK, 'สินค้าหมด'),
        (ALMOST_OUT_OF_STOCK, 'สินค้าเกือบหมด'),
        (INSTOCK, 'สินค้าพร้อมขาย')
    )

    DESSERT = 1
    DRINK = 2
    FOOD = 3
    TYPE_PRODUCT = (
        (DESSERT, 'ของหวาน'),
        (DRINK, 'เครื่องดื่ม'),
        (FOOD, 'อาหาร'),
    )

    SPICY = 1
    SWEET = 2
    FLAVOUR = (
        (SPICY, 'เผ็ด'),
        (SWEET, 'หวาน')
    )
    old_product = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, default=None)
    img = models.ImageField(
        _("Image"), upload_to=upload_to_product, default=None, null=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    flavour_level = models.BooleanField(default=False)
    status = models.IntegerField(default=INSTOCK, choices=STATUS_STOCK)
    remain = models.IntegerField(default=0)
    flavour = models.IntegerField(choices=FLAVOUR)
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=None, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    type_product = models.IntegerField(choices=TYPE_PRODUCT, default=FOOD)
    topping_category = models.ForeignKey(ToppingCategory,on_delete=models.PROTECT, default=None, null=True)
    warehouse = models.IntegerField(choices=WAREHOUSE, default=NONE_PICK_UP)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, null=True, default=None)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="product_create_by")

    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="product_update_by", 
        null=True, blank=True, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True, default=None)


class AddProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="add_product_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="add_product_update_by", null=True, blank=True,default=None)


class PriceProduct(models.Model):
    status = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_channel = models.ForeignKey(SaleChannel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.ForeignKey(
        'self', on_delete=models.PROTECT, null=True, blank=True)


