from django.db import models
from backend.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _ 
from raw_material.models import Unit

def upload_to_material(instance,filename):
    return 'material/{filename}'.format(filename=filename)

class MaterialCategory(models.Model):
    status = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True,blank=True)
    type_category = models.CharField(max_length=30)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="material_category_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="material_category_update_by",null=True,blank=True)
    


class Material(models.Model):
    img = models.ImageField(_("Image"), upload_to=upload_to_material)
    status = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True,blank=True)
    category = models.ForeignKey(MaterialCategory, on_delete=models.PROTECT)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="material_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="material_update_by",null=True,blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    minimum = models.IntegerField(default=1)


class PickUpMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pick_up_material_create_by")

class AddMaterial(models.Model):
    material = models.ForeignKey(Material,on_delete=models.PROTECT)
    amount = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True,blank=True)
    create_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="add_material_create_by")
    update_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="add_material_update_by", null=True,blank=True)




