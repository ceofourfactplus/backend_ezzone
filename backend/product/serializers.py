import datetime
from os import read
from django.db.models import fields
from rest_framework import serializers
from product.models import ProductCategory, SaleChannel, Product, PriceProduct, SetTopping, ToppingCategory, Topping, PriceTopping
from raw_material.serializers import UnitSerializer
from user.serializers import UserSerializer
from pprint import pprint
from promotion.models import PricePackage, PromotionPackage
from promotion.serializers import PackageListSerializer
from promotion.models import PackageItem, PromotionPackage,ItemTopping

class PricePackageS(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    package_set = PackageListSerializer()
    class Meta: 
        model = PricePackage
        fields = [
            'id',
            'normal_price',
            'discount_price',
            'sale_channel',
            'package',
            'package_set'
        ]
        read_only_fields = ('package',)

class PricePackageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    packages = PackageListSerializer(read_only=True)
    class Meta:
        model = PricePackage
        fields = [
            'id',
            'normal_price',
            'discount_price',
            'sale_channel',
            'package',
            'packages'
        ]
        read_only_fields = ('sale_channel',)


class UpdateImageSaleS(serializers.ModelSerializer):
    class Meta:
        model = SaleChannel
        fields = ['img']


class ImageTopping(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['img']


class ToppingS(serializers.ModelSerializer):

    # all id
    unit_id = serializers.IntegerField()
    old_product_id = serializers.IntegerField(allow_null=True, required=False)
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField(allow_null=True, required=False)
    # pricetopping_set = PriceToppingSerializer(read_only=True, many=True)
    # # all set
    # unit_set = UnitSerializer(read_only=True, source='unit')
    # old_product_set = serializers.IntegerField(allow_null=True, required=False)
    # create_by_set = UserSerializer(read_only=True, source='create_by')
    # update_by_set = UserSerializer(read_only=True, source='update_by')

    class Meta:
        model = Topping
        fields = [
            'id', 'img', 'code', 'name', 'is_active', 'status',
            'remain', 'minimum', 'maximum', 'type_topping', 'warehouse', 'create_at',
            # all set
            # 'unit_set', 'create_by_set',
            # 'update_by_set', 'old_product_set', 'pricetopping_set',

            # all id
            'old_product_id',
            'unit_id', 'create_by_id',
            'update_by_id',
        ]


class ProductS(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    unit_id = serializers.IntegerField()
    old_product_id = serializers.IntegerField(allow_null=True, required=False)
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField(allow_null=True, required=False)
    topping_category_id = serializers.IntegerField(
        allow_null=True, required=False)
    class Meta:
        model = Product
        fields = [
            'id', 'img', 'code', 'name',
            'is_active', 'flavour_level', 'status',
            'remain', 'flavour', 'minimum', 'maximum',
            'topping_category_id', 'warehouse', 'create_at',
            'update_at', 'type_product',

            # all id
            'old_product_id',
            'unit_id', 'category_id', 'create_by_id',
            'update_by_id',
        ]


class PriceToppingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    topping_set = ToppingS(read_only=True, source="topping")

    class Meta:
        model = PriceTopping
        fields = ["id", "price", "topping",
                  "sale_channel", "status", 'topping_set']
        read_only_fields = ('sale_channel',)


class PriceProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product_set = ProductS(read_only=True, source="product")

    class Meta:
        model = PriceProduct
        fields = ["id", "price", "product",
                  "sale_channel", "status", 'product_set']
        read_only_fields = ('sale_channel',)


class OnlyPriceProduct(serializers.ModelSerializer):
    class Meta:
        model = PriceProduct
        fields = ["id", "price", "product",
                  "sale_channel", "status"]


class OnlyPriceTopping(serializers.ModelSerializer):
    class Meta:
        model = PriceTopping
        fields = ["id", "price", "topping",
                  "sale_channel", "status"]


class ToppingSerializer(serializers.ModelSerializer):

    # all id
    unit_id = serializers.IntegerField()
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField(allow_null=True, required=False)
    pricetopping_set = OnlyPriceTopping(read_only=True, many=True)
    # all set
    unit_set = UnitSerializer(read_only=True, source='unit')
    create_by_set = UserSerializer(read_only=True, source='create_by')
    update_by_set = UserSerializer(read_only=True, source='update_by')
    img = serializers.ImageField(read_only=True)

    class Meta:
        model = Topping
        fields = [
            'id', 'img', 'code', 'name', 'is_active', 'status',
            'remain', 'minimum', 'pricetopping_set', 'maximum', 'type_topping', 'warehouse', 'create_at',
            # all set
            'unit_set', 'create_by_set',
            'update_by_set',

            # all id
            'unit_id', 'create_by_id',
            'update_by_id',
        ]


class SetToppingSerializer(serializers.ModelSerializer):
    topping_set = ToppingSerializer(read_only=True, source="topping")

    class Meta:
        model = SetTopping
        fields = ['category', 'topping', 'topping_set']


class ToppingCategorySerializer(serializers.ModelSerializer):
    settopping_set = SetToppingSerializer(read_only=True, many=True)

    class Meta:
        model = ToppingCategory
        fields = ['id', 'category',
                  'create_by', 'update_by', 'settopping_set']


class GetterSaleChannel(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    img = serializers.ImageField(read_only=True)

    class Meta:
        model = SaleChannel
        fields = ['id', 'sale_channel', 'gp', 'img',
                  'status', 'create_by', 'update_by',
                  'create_at', 'update_at']

class SaleChannelS(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    img = serializers.ImageField(read_only=True)

    class Meta:
        model = SaleChannel
        fields = ['id', 'sale_channel', 'gp', 'img',
                  'status', 'create_by', 'update_by',
                  'create_at', 'update_at',
                  ]


class PricePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePackage
        fields = ['id', 'discount_price',
                  'normal_price', 'sale_channel', 'package']
        read_only_fields = ('package',)


class ItemToppingSerializer(serializers.ModelSerializer):
    topping_set = ToppingS(read_only=True,source='topping')
    class Meta:
        model = ItemTopping
        read_only_fields = ('item',)
        fields = ['id', 'item', 'total_price','topping', 'qty','topping_set']


class PackageItemSerializer(serializers.ModelSerializer):
    product_set = ProductS(read_only=True,source='product')
    itemtopping_set = ItemToppingSerializer(many=True)
    class Meta:
        model = PackageItem
        fields = ['id', 'qty', 'total_price', 'package',
                  'description', 'product', 'itemtopping_set','product_set']
        read_only_fields = ('package',)


class PackageSerializer(serializers.ModelSerializer):
    packageitem_set = PackageItemSerializer(many=True)
    pricepackage_set = PricePackageSerializer(many=True)
    img = serializers.ImageField(read_only=True)

    class Meta:
        model = PromotionPackage
        fields = ['id', 'promotion', 'start_date', 'status',
                  'description', 'create_at', 'create_by',
                  'update_at', 'update_by', 'total_amount', 'amount_day', 'img', 'packageitem_set', 'pricepackage_set']

    def create(self, validated_data):
        packageitem_set = validated_data.pop('packageitem_set')
        pricepackage_set = validated_data.pop('pricepackage_set')
        package = PromotionPackage.objects.create(**validated_data)
        for item in packageitem_set:
            topping = item.pop('itemtopping_set')
            items = PackageItem.objects.create(**item, package=package)
            for t in topping:
                ItemTopping.objects.create(**t, item=items)
        for price in pricepackage_set:
            PricePackage.objects.create(**price, package=package)
        return package

    def update(self, instance, validated_data):
        print(validated_data.items())
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        package_item_id = [i['id']
                           for i in validated_data['packageitem_set'] if i.get('id')]
        PackageItem.objects.filter(package_id=instance.id).exclude(
            id__in=package_item_id).delete()

        to_be_create = [
            i for i in validated_data['packageitem_set'] if i.get('id') == None]
        for i in to_be_create:
            if 'itemtopping_set' in i:
                itemtopping_set = i.pop('itemtopping_set')
            package_item = PackageItem.objects.create(
                **i, package_id=instance.id)
            for p in itemtopping_set:
                ItemTopping.objects.create(**p, item_id=package_item.id)

        to_be_update = [
            i for i in validated_data['packageitem_set'] if i.get('id')]
        for i in to_be_update:
            if 'itemtopping_set' in i:
                itemtopping_set = i.pop('itemtopping_set')
            pi = PackageItem.objects.filter(
                id=i['id']).update(**i, package_id=instance.id)
            to_be_create_topping = [
                i for i in itemtopping_set if i.get("id") == None]
            for p in to_be_create_topping:
                ItemTopping.objects.create(**p, item_id=pi.id)

            to_be_delete_topping = [p['id'] for p in itemtopping_set]
            for p in to_be_delete_topping:
                ItemTopping.objects.filter(item_id=i['id']).exclude(
                    id__in=to_be_delete_topping).delete()

            to_be_update_topping = [p for p in itemtopping_set]
            for p in to_be_update_topping:
                print(p, 'p')
                ItemTopping.objects.filter(id=p['id']).update(**p)
        return validated_data

class PricePackageForSaleChannel(serializers.ModelSerializer):
    class Meta:
        model = PricePackage
        fields = ['id', 'discount_price',
                  'normal_price', 'sale_channel', 'package']
        read_only_fields = ('sale_channel',)


class SaleChannelSerializer(serializers.ModelSerializer):
    price_topping = PriceToppingSerializer(many=True, source="pricetopping")
    price_product = PriceProductSerializer(many=True, source="priceproduct")
    price_package = PricePackageForSaleChannel(many=True,source="pricepackage_set")
    id = serializers.IntegerField(required=False)
    img = serializers.ImageField(read_only=True)
    can_delete = serializers.BooleanField(read_only=True, required=False)
    qty = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = SaleChannel
        fields = ['id', 'sale_channel', 'gp', 'img',
                  'status', 'create_by', 'update_by',
                  'create_at', 'update_at', 'price_topping', 'price_product', 
                  'price_package', 'can_delete',
                  'qty'
                  ]

    def create(self, validated_data):
        price_toppings = validated_data.pop('pricetopping')
        price_products = validated_data.pop('priceproduct')
        price_packages = validated_data.pop('pricepackage_set')
        sale_channel = SaleChannel.objects.create(**validated_data)
        print('finish')
        for price_topping in price_toppings:
            PriceTopping.objects.create(
                **price_topping, sale_channel=sale_channel)

        for price_product in price_products:
            PriceProduct.objects.create(
                **price_product, sale_channel=sale_channel)

        for price_package in price_packages:
            PricePackage.objects.create(
                **price_package, sale_channel=sale_channel)
        return sale_channel

    def update(self, instance, validated_data):
        instance.sale_channel = validated_data['sale_channel']
        instance.gp = validated_data['gp']
        instance.status = validated_data['status']
        instance.update_by = validated_data['update_by']
        instance.update_at = datetime.datetime.now()
        instance.save()

        # create update delete pricetopping
        pricetopping_id = [c['id']
                           for c in validated_data['pricetopping'] if c.get('id')]
        PriceTopping.objects.filter(sale_channel_id=instance.id).exclude(
            id__in=pricetopping_id).delete()

        to_be_create_topping = [
            c for c in validated_data['pricetopping'] if c.get('id') == None]
        for p in to_be_create_topping:
            PriceTopping.objects.create(**p, sale_channel_id=instance.id)

        to_be_update_topping = [
            c for c in validated_data['pricetopping'] if c.get('id')]
        for p in to_be_update_topping:
            PriceTopping.objects.filter(id=p['id']).update(**p)

        # create update delete priceproduct

        priceproduct_id = [c['id']
                           for c in validated_data['priceproduct'] if c.get('id')]
        PriceProduct.objects.filter(sale_channel_id=instance.id).exclude(
            id__in=priceproduct_id).delete()

        to_be_create = [
            c for c in validated_data['priceproduct'] if c.get('id') == None]
        for p in to_be_create:
            PriceProduct.objects.create(**p, sale_channel_id=instance.id)

        to_be_update = [
            c for c in validated_data['priceproduct'] if c.get('id')]
        for p in to_be_update:
            PriceProduct.objects.filter(id=p['id']).update(**p)

        pricepackage_id = [c['id']
                           for c in validated_data['pricepackage_set'] if c.get('id')]
        PricePackage.objects.filter(sale_channel_id=instance.id).exclude(
            id__in=pricepackage_id).delete()

        to_be_create = [
            c for c in validated_data['pricepackage_set'] if c.get('id') == None]
        for p in to_be_create:
            PricePackage.objects.create(**p, sale_channel_id=instance.id)

        to_be_update = [
            c for c in validated_data['pricepackage_set'] if c.get('id')]
        for p in to_be_update:
            PricePackage.objects.filter(id=p['id']).update(**p)

        return instance


class ProductCategorySerializer(serializers.ModelSerializer):
    product_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'category', 'type_category',
                  'create_by', 'update_by', 'product_set']


class OnlyProductCategory(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category', 'type_category',
                  'create_by', 'update_by']


class ImageProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['img']


class ProductSerializer(serializers.ModelSerializer):

    # all id
    category_id = serializers.IntegerField()
    unit_id = serializers.IntegerField()
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField(allow_null=True, required=False)
    topping_category_id = serializers.IntegerField(
        allow_null=True, required=False)
    # all set
    category_set = OnlyProductCategory(read_only=True, source='category')
    unit_set = UnitSerializer(read_only=True, source='unit')
    priceproduct_set = OnlyPriceProduct(many=True, read_only=True)
    topping_category_set = ToppingCategorySerializer(
        read_only=True, source="topping_category")
    img = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'img', 'code', 'name',
            'is_active', 'flavour_level', 'status',
            'remain', 'flavour', 'minimum', 'maximum',
            'topping_category_id', 'warehouse', 'create_at',
            'update_at', 'priceproduct_set', 'type_product',

            # all set
            'unit_set', 'category_set',  'topping_category_set',

            # all id
            'unit_id', 'category_id', 'create_by_id',
            'update_by_id',
        ]


class ProductReportSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'img']


class ChannelReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleChannel
        fields = ['id', 'sale_channel', 'img']
