import re
from tkinter.tix import Tree
from django.db.models import fields
from rest_framework import serializers
from user.serializers import UserSerializer
from product.models import Product, Topping
from customer.serializers import CustomerSerializer, AddressCustomerSerializer
from .models import PointPromotion, Voucher, PricePackage, PromotionPackage, PackageItem, ItemTopping, Rewards, ConditionRewards, Redemption, CustomerPoint, ExchangeHistory
from pprint import pprint


class ToppingS(serializers.ModelSerializer):

    # all id
    unit_id = serializers.IntegerField()
    old_product_id = serializers.IntegerField(allow_null=True, required=False)
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Topping
        fields = [
            'id', 'img', 'code', 'name', 'is_active', 'status',
            'remain', 'minimum', 'maximum', 'type_topping', 'warehouse', 'create_at',

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


class PricePackageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = PricePackage
        fields = ['id', "package", "sale_channel",
                  'normal_price', 'discount_price']
        read_only_fields = ('package',)


class PointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointPromotion
        fields = '__all__'


class VoucherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'


class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionPackage
        fields = '__all__'


class PromotionPackageImage(serializers.ModelSerializer):
    class Meta:
        model = PromotionPackage
        fields = ['img']


class PointSerializer(serializers.ModelSerializer):
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField()
    create_by_set = UserSerializer(read_only=True, source="user")
    update_by_set = UserSerializer(read_only=True, source="user")

    class Meta:
        model = PointPromotion
        fields = [
            'id',
            'promotion',
            'start_promotion_date',
            'end_promotion_date',
            'end_reward_redemption',
            'price_per_point',
            'point',
            'status',
            'description',
            'create_by_id',
            'update_by_id',
            'create_by_set',
            'update_by_set',
            'create_at',
            'update_at',
        ]


class VoucherSerializer(serializers.ModelSerializer):
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField()

    class Meta:
        model = Voucher
        fields = [
            'id',
            'voucher',
            'code',
            'img',
            'discount',
            'start_date',
            'end_date',
            'is_percent',
            'description',
            'qty',
            'status',
            'create_by_id',
            'update_by_id',
            'create_at',
            'update_at',
        ]


# class ItemToppingSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)
#     topping_id = serializers.IntegerField()
#     item_id = serializers.IntegerField(read_only=True)
#     topping_set = ToppingS(read_only=True, source='topping')

#     class Meta:
#         model = ItemTopping
#         fields = [
#             'id',
#             'topping_id',
#             'qty',
#             'total_price',
#             'item_id',
#             'topping_set',
#         ]


# class PackageItemSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)
#     product_id = serializers.IntegerField()
#     package_id = serializers.IntegerField(read_only=True)
#     product_set = ProductS(read_only=True, source='product')
#     itemtopping_set = ItemToppingSerializer(
#         many=True, required=False, allow_null=True)
#     description = serializers.CharField(required=False, allow_blank=True)

#     class Meta:
#         model = PackageItem
#         fields = [
#             'id',
#             'product_id',
#             'qty',
#             'total_price',
#             'description',
#             'package_id',
#             'product_set',
#             'itemtopping_set',
#         ]

# class PromotionPackageSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)
#     create_by_id = serializers.IntegerField()
#     update_by_id = serializers.IntegerField()
#     description = serializers.CharField(required=False, allow_blank=True)
#     packageitem_set = PackageItemSerializer(many=True)
#     img = serializers.ImageField(read_only=True)
#     pricepackage_set = PricePackageSerializer(many=True,source='pricepackage')

#     class Meta:
#         model = PromotionPackage
#         fields = [
#             'id',
#             'img',
#             'start_date',
#             'promotion',
#             'amount_day',
#             'status',
#             'total_amount',
#             'description',
#             'create_by_id',
#             'update_by_id',
#             'create_at',
#             'update_at',
#             'packageitem_set',
#             'img',
#             'pricepackage_set'
#         ]

#     def create(self, validated_data):
#         packageitem_set = validated_data.pop('packageitem_set')
#         pricepackage_set = validated_data.pop('pricepackage')
#         pprint(pricepackage_set)
#         pp = PromotionPackage.objects.create(**validated_data)
#         if packageitem_set != []:
#             for item in packageitem_set:
#                 itemtopping_set = item.pop('itemtopping_set')
#                 package_item = PackageItem.objects.create(**item, package=pp)
#                 if not itemtopping_set == []:
#                     for topping in itemtopping_set:
#                         ItemTopping.objects.create(
#                             **topping, item=package_item)
#         for pricepackage in pricepackage_set:
#             PricePackage.objects.create(**pricepackage, package=pp)
#         return pp

#     def update(self, instance, validated_data):
#         instance.promotion = validated_data['promotion']
#         instance.start_date = validated_data['start_date']
#         instance.amount_day = validated_data['amount_day']
#         instance.status = validated_data['status']
#         instance.total_amount = validated_data['total_amount']
#         instance.description = validated_data['description']
#         instance.update_by_id = validated_data['update_by_id']
#         instance.save()

#         package_item_id = [i['id']
#                            for i in validated_data['packageitem'] if i.get('id')]
#         PackageItem.objects.filter(package_id=instance.id).exclude(
#             id__in=package_item_id).delete()
#         print(validated_data['packageitem_set'], 'validated_data')
#         to_be_create = [
#             i for i in validated_data['packageitem_set'] if i.get('id') == None]
#         for i in to_be_create:
#             if 'itemtopping_set' in i:
#                 itemtopping_set = i.pop('itemtopping_set')
#             package_item = PackageItem.objects.create(
#                 **i, package_id=instance.id)
#             for p in itemtopping_set:
#                 ItemTopping.objects.create(**p, item_id=package_item.id)

#         to_be_update = [
#             i for i in validated_data['packageitem_set'] if i.get('id')]
#         for i in to_be_update:
#             if 'itemtopping_set' in i:
#                 itemtopping_set = i.pop('itemtopping_set')
#             pi = PackageItem.objects.filter(
#                 id=i['id']).update(**i, package_id=instance.id)
#             to_be_create_topping = [
#                 i for i in itemtopping_set if i.get("id") == None]
#             for p in to_be_create_topping:
#                 ItemTopping.objects.create(**p, item_id=pi.id)

#             to_be_delete_topping = [p['id'] for p in itemtopping_set]
#             for p in to_be_delete_topping:
#                 ItemTopping.objects.filter(item_id=i['id']).exclude(
#                     id__in=to_be_delete_topping).delete()

#             to_be_update_topping = [p for p in itemtopping_set]
#             for p in to_be_update_topping:
#                 print(p, 'p')
#                 ItemTopping.objects.filter(id=p['id']).update(**p)
#         return validated_data


class RewardsSerializer(serializers.ModelSerializer):
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField()

    class Meta:
        model = Rewards
        fields = [
            'id',
            'reward',
            'img',
            'value',
            'description',
            'qty',
            'point',
            'cost',
            'status',
            'is_pre_order',
            'create_by_id',
            'update_by_id',
            'create_at',
            'update_at',
        ]


class ConditionRewardsSerializer(serializers.ModelSerializer):
    point_promotion_id = serializers.IntegerField()
    reward_id = serializers.IntegerField()
    point_promotion_set = PointSerializer(
        read_only=True, source='point_promotion')
    reward_set = RewardsSerializer(read_only=True, source='reward')

    class Meta:
        model = ConditionRewards
        fields = [
            'id',
            'point_promotion_id',
            'reward_id',
            'point_promotion_set',
            'reward_set',
            'point',
        ]


class RedemptionSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    reward_id = serializers.IntegerField()
    deal_user_id = serializers.IntegerField()
    deliver_user_id = serializers.IntegerField()
    point_promotion_id = serializers.IntegerField()
    point_promotion_set = PointSerializer(
        read_only=True, source='point_promotion')
    reward_set = RewardsSerializer(read_only=True, source='reward')
    deal_user_set = UserSerializer(read_only=True, source="user")
    deliver_user_set = UserSerializer(read_only=True, source="user")
    customer_set = CustomerSerializer(read_only=True, source="user")

    class Meta:
        model = Redemption
        fields = [
            'id',
            'customer_id',
            'reward_id',
            'deal_user_id',
            'deliver_user_id',
            'point_promotion_id',
            'status_given',
            'point',
            'due_date',
            'description',
            'create_at',
            'img',
            'point_promotion_set',
            'reward_set',
        ]


class CustomerPointSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    point_promotion_id = serializers.IntegerField()
    customer_set = CustomerSerializer(read_only=True, source="customer")
    point_promotion_set = PointSerializer(
        read_only=True, source='point_promotion')

    class Meta:
        model = CustomerPoint
        fields = [
            'id',
            'point',
            'description',
            'customer_id',
            'point_promotion_id',
            'customer_set',
            'point_promotion_set',
        ]


class ExchangeHistorySerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    reward_id = serializers.IntegerField()
    create_by_id = serializers.IntegerField()
    update_by_id = serializers.IntegerField()
    create_by_set = UserSerializer(read_only=True, source="user")
    customer_set = CustomerSerializer(read_only=True, source="customer")
    reward_set = RewardsSerializer(read_only=True, source='reward')

    class Meta:
        model = ExchangeHistory
        fields = [
            'id',
            'point',
            'qty',
            'signature',
            'customer_id',
            'reward_id',
            'customer_set',
            'reward_set',
            'create_by_set',
            'create_at',
            'create_by_id',
            'update_by_id',
        ]
