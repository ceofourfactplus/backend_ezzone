from django.db import models
from django.utils.translation import gettext_lazy as _


def upload_to_customer(instance,filename):
    return 'customer/{filename}'.format(filename=str(instance.nick_name)+'_'+str(instance.first_name)+'.png')


class Customer(models.Model):
    nick_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=100,null=True,blank=True,default=None)
    last_name = models.CharField(max_length=255, null=True,default=None)
    phone_number = models.CharField(max_length=13)
    gender = models.CharField(max_length=50,null=True,blank=True,default=None)
    img = models.ImageField(_("Image"),upload_to=upload_to_customer,null=True,blank=True,default=None)
    email = models.EmailField(null=True,blank=True,default=None)
    birth_date = models.DateField(null=True,blank=True,default=None)
    line_customer_id = models.CharField(max_length=100,null=True,blank=True,default=None)
    invited_by = models.ForeignKey('self',on_delete=models.PROTECT,null=True,blank=True,default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_joined = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
class AddressCustomer(models.Model):
    HOME = 1
    WORK = 2
    OTHER = 3
    STATUS_ADDRESS = (
        (HOME,'home'),
        (WORK,'work'),
        (OTHER,'other')
    )
    address = models.TextField()
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    status_address = models.IntegerField(choices=STATUS_ADDRESS,default=HOME)
    status = models.BooleanField(default=True) 
    
# class LevelCustomer(models.Model):
#     level = models.CharField
#     price = models.DecimalField
#     time = models.TextField
