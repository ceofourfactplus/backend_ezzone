from django.db import models
from backend.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _


def upload_to_raw_material(instance, filename):
    return 'raw_material/{filename}'.format(filename=filename)


def upload_to_supplier(instance, filename):
    return 'supplier/{filename}'.format(filename=filename)


class RawMaterialCategory(models.Model):
    name = models.CharField(max_length=255)


class Unit(models.Model):
    unit = models.CharField(max_length=30)


class Supplier(models.Model):
    company_name = models.CharField(max_length=255)  # company_name
    contact = models.CharField(max_length=100)  # ติดต่อใคร
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=500)
    email = models.EmailField(null=False, blank=False,default=None)
    google_map = models.URLField(max_length=400, default='')
    create_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(blank=True, null=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="supplier_create_by")
    update_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  related_name="supplier_update_by", blank=True, null=True)
    img = models.ImageField(
        _("Image"), upload_to=upload_to_supplier, default='supplier/default.jpg')


class RawMaterial(models.Model):
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.PROTECT)
    status = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    remain = models.IntegerField(null=True, blank=True, default=None)
    minimum = models.IntegerField(null=True, blank=True, default=None)
    maximum = models.IntegerField(null=True, blank=True, default=None)
    in_refrigerator = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="raw_material_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="raw_material_update_by", null=True, blank=True, default=None)
    img = models.ImageField(
        _("Image"), upload_to=upload_to_raw_material, default=None, null=True)
    unit_l = models.ForeignKey(Unit, on_delete=models.PROTECT,
                               related_name="raw_material_unit_l", null=True, blank=True, default=None)
    unit_m = models.ForeignKey(Unit, on_delete=models.PROTECT,
                               related_name="raw_material_unit_m", null=True, blank=True, default=None)
    unit_s = models.ForeignKey(Unit, on_delete=models.PROTECT,
                               related_name="raw_material_unit_s", null=True, blank=True, default=None)
    m_to_l = models.IntegerField(null=True, blank=True, default=None)
    s_to_m = models.IntegerField(null=True, blank=True, default=None)
    avg_l = models.DecimalField(
        max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    avg_m = models.DecimalField(
        max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    avg_s = models.DecimalField(
        max_digits=5, decimal_places=2, default=None, null=True, blank=True)


class PriceRawMaterial(models.Model):
    avg_price = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    last_price = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    raw_material = models.ForeignKey(
        RawMaterial, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(
        Unit, on_delete=models.PROTECT, null=True, blank=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, null=True, blank=True)


class PickUpRawMaterial(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT)
    amount = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pick_up_raw_material_create_by")


class ReceiptRawMaterial(models.Model):
    CASH = "cash"
    TRANSFER = "transfer"
    PAYMENT = (
        (CASH, 'จ่ายสด'),
        (TRANSFER, 'โอน')
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.IntegerField()
    payment = models.CharField(max_length=8, choices=PAYMENT)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="receipt_raw_material_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="receipt_raw_material_update_by", null=True, blank=True)


class ReceiptRawMaterialDetail(models.Model):
    receipt_raw_material = models.ForeignKey(
        ReceiptRawMaterial, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.IntegerField()
    remark = models.TextField(blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="receipt_raw_material_detail_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="receipt_raw_material_detail_update_by", null=True, blank=True)


class PO(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    amount = models.IntegerField()
    status = models.BooleanField(default=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    last_price = models.DecimalField(max_digits=5, decimal_places=2)
