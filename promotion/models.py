from django.db import models
from django.utils.translation import gettext_lazy as _
from customer.models import Customer
from backend.settings import AUTH_USER_MODEL
from product.models import Product, Topping, SaleChannel

def upload_to_promotion(instance,filename):
    return 'promotion/{filename}'.format(filename=filename)

def upload_to_rewards(instance,filename):
    return 'rewards/{filename}'.format(filename=filename)

def upload_to_voucher(instance,filename):
    return 'voucher/{filename}'.format(filename=filename)

def upload_to_redemption(instance,filename):
    return 'redemption/{filename}'.format(filename=filename)
  
def upload_to_package(instance,filename):
    return 'package/{filename}'.format(filename=filename)

def upload_to_history(instance,filename):
    return 'history/{filename}'.format(filename=filename)

class PointPromotion(models.Model):
  promotion = models.CharField(max_length=100)
  start_promotion_date = models.DateField()
  end_promotion_date = models.DateField()
  end_reward_redemption = models.DateField()
  price_per_point = models.IntegerField()
  point = models.IntegerField(default=1)
  status = models.BooleanField(default=False)
  description = models.TextField(null=True,blank=True)
  create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="promotion_point_create_by")
  update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="promotion_point_update_by",null=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(null=True,blank=True)
    

class Rewards (models.Model):
  reward = models.CharField(max_length=100)
  img = models.ImageField(_("Image"), upload_to=upload_to_rewards, null=True, blank=True)
  value = models.DecimalField(max_digits=4,decimal_places=2)
  description = models.TextField(null=True,blank=True)
  qty = models.IntegerField()
  point = models.IntegerField()
  cost = models.DecimalField(max_digits=4,decimal_places=2)
  status = models.BooleanField(default=True)
  is_pre_order = models.BooleanField(default=False)
  create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="rewards_create_by")
  update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="rewards_update_by",null=True,blank=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(null=True,blank=True)
    

class ConditionRewards(models.Model):
  point_promotion = models.ForeignKey(PointPromotion,on_delete=models.CASCADE)
  reward  = models.ForeignKey(Rewards,on_delete=models.CASCADE)
  point = models.IntegerField()


class Voucher(models.Model):
  voucher = models.CharField(max_length=100)
  code = models.CharField(max_length=100)
  img = models.ImageField(_("Image"), upload_to=upload_to_voucher, null=True, blank=True)
  discount = models.DecimalField(max_digits=6,decimal_places=2)
  start_date = models.DateField()
  end_date = models.DateField()
  is_percent = models.BooleanField(default=False)
  description = models.TextField(null=True,blank=True)
  qty = models.IntegerField(default=1)
  status = models.BooleanField(default=True)
  create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="voucher_create_by")
  update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="voucher_update_by",null=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now_add=True,null=True)
    

class Redemption(models.Model):
  customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
  reward = models.ForeignKey(Rewards,on_delete=models.PROTECT)
  deal_user =  models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT, related_name="redemption_deal_user")
  deliver_user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT, related_name="redemption_deliver_user")
  point_promotion = models.ForeignKey(PointPromotion,on_delete=models.PROTECT)
  create_at = models.DateTimeField(auto_now_add=True)
  point =  models.IntegerField()
  status_given = models.BooleanField(default=False)
  due_date = models.DateTimeField(null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  img = models.ImageField(_("Image"), upload_to=upload_to_redemption, null=True, blank=True)


class PromotionPackage(models.Model):
  promotion = models.CharField(max_length=100)
  start_date = models.DateField()
  img = models.ImageField(_("Image"), upload_to=upload_to_package, null=True, blank=True)
  amount_day = models.IntegerField()
  status = models.BooleanField(default=True)
  total_amount = models.IntegerField()
  description = models.TextField(null=True,blank=True)
  create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="promotion_package_create_by")
  update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="promotion_package_update_by",null=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now_add=True,null=True)

class PackageItem(models.Model):
  product = models.ForeignKey(Product,on_delete=models.PROTECT)
  qty = models.IntegerField(default=1)
  total_price = models.DecimalField(max_digits=6,decimal_places=2)
  description = models.TextField(null=True,blank=True)
  package = models.ForeignKey(PromotionPackage,on_delete=models.CASCADE)

class ItemTopping(models.Model):
  topping = models.ForeignKey(Topping,on_delete=models.PROTECT)
  item = models.ForeignKey(PackageItem,on_delete=models.CASCADE)
  qty = models.IntegerField()
  total_price = models.DecimalField(max_digits=4,decimal_places=2)
#   description = models.TextField(null=True,blank=True)

class PricePackage(models.Model):
	sale_channel = models.ForeignKey(SaleChannel,on_delete=models.CASCADE)
	normal_price = models.DecimalField(max_digits=6,decimal_places=2)
	discount_price = models.DecimalField(max_digits=6,decimal_places=2)
	package = models.ForeignKey(PromotionPackage,on_delete=models.CASCADE)

class CustomerPoint(models.Model):
  customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
  point_promotion = models.ForeignKey(PointPromotion,on_delete=models.PROTECT)
  point = models.IntegerField()
  description = models.TextField(null=True,blank=True)

class ExchangeHistory(models.Model):
  customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
  reward = models.ForeignKey(Rewards,on_delete=models.PROTECT)
  point = models.IntegerField()
  qty = models.IntegerField()
  signature = models.ImageField(_("Image"), upload_to=upload_to_history, null=True, blank=True)
  create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="exchange_history_create_by")
  update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="exchange_history_update_by",null=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now_add=True,null=True)