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

class SaleChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleChannel
        fields = '__all__'

class ProductCategorySerializer(DynamicModelSerializer):
    class Meta:
        model = ProductCategory
        name = 'product_category'
        fields = '__all__'

class ProductListSerializer(DynamicModelSerializer):
    class Meta:
        model = Product
        name = 'product'
        fields = ("id", "img", "name", "total_times")

class ProductSerializer(DynamicModelSerializer):
    class Meta:
        model = Product
        name = 'product'
        fields = '__all__'

    unit = DynamicRelationField('UnitSerializer', embed=True) 
    category = DynamicRelationField('ProductCategorySerializer', embed=True) 
    sale_chanenl = DynamicRelationField('ProductCategorySerializer', embed=True) 

class ToppingSerializer(DynamicModelSerializer):
    class Meta:
        model = Topping
        name = 'topping'
        fields = '__all__'

    unit = DynamicRelationField('UnitSerializer', embed=True) 

