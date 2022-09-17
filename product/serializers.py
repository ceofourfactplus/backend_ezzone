import datetime
from operator import mod
from os import read
from re import T
from unicodedata import name
from django.db.models import fields
from rest_framework import serializers
from product.models import ProductCategory, SaleChannel, Product, PriceProduct, SetTopping, ToppingCategory, Topping, PriceTopping
from raw_material.serializers import UnitSerializer
from user.serializers import UserSerializer
from pprint import pprint
from promotion.models import PricePackage, PromotionPackage
from promotion.serializers import PackageListSerializer
from promotion.models import PackageItem, PromotionPackage, ItemTopping

class ProductListSerializer(DynamicModelSerializer):
    class Meta:
        model = Product
        name = 'product'
        fields = ("img", )