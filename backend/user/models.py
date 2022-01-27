from django.contrib.auth.models import AbstractUser
from django.db import models
from backend.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _ 

def upload_to_user(instance,filename):
    return 'user/{filename}'.format(filename=instance.username)

class User(AbstractUser):
  NOT_WORKING = 0
  WORKING = 1
  BANNED = 2
  STATUS_WORK = (
    (NOT_WORKING,'not working'),
    (WORKING,'working'),
    (BANNED,'banned'),
  )
  nick_name = models.CharField(max_length=30)
  is_chef = models.BooleanField(default=False)
  is_barista = models.BooleanField(default=False)
  is_purchesing = models.BooleanField(default=False)
  is_receptionist = models.BooleanField(default=False)
  is_owner = models.BooleanField(default=False)
  birth_date = models.DateField(blank=True,null=True)
  is_working = models.IntegerField(default=WORKING,choices=STATUS_WORK)
  gender = models.CharField(max_length=30)
  address = models.TextField()
  id_card = models.CharField(blank=True,null=True,max_length=13)
  img = models.ImageField(_("Image"), upload_to=upload_to_user,default='',null=True,blank=True)

class Login(models.Model):
  token = models.CharField(max_length=30,default=None)
  user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT,default=None,)
  login_at = models.DateTimeField(auto_now_add=True)
  logout_at = models.DateTimeField(default=None,null=True)
  time_login = models.TimeField(default=None,null=True)