import datetime
from pos.models import Order, OrderItem, OrderItemTopping, Payment
from rest_framework import serializers
from customer.serializers import CustomerSerializer, AddressCustomerSerializer
from product.serializers import ProductSerializer, ToppingSerializer, GetterSaleChannel
from product.serializers import PackageSerializer
from pprint import pprint


class PaymentSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_blank=True, required=False)
    is_used = serializers.BooleanField(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'


class OrderItemToppingSerializer(serializers.ModelSerializer):
    topping_set = ToppingSerializer(read_only=True, source="topping")
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItemTopping
        fields = [
            "id",
            "topping",
            'price_topping',
            "total_price",
            "amount",
            "topping_set",
            'item'
        ]
        read_only_fields = ('item',)


class OrderItemSerializer(serializers.ModelSerializer):
    product_set = ProductSerializer(read_only=True, source='product')
    topping_set = ToppingSerializer(read_only=True, source="topping")
    package_set = PackageSerializer(read_only=True, source="package")
    id = serializers.IntegerField(required=False)
    orderitemtopping_set = OrderItemToppingSerializer(
        many=True, required=False, allow_null=True)
    description = serializers.CharField(allow_blank=True, required=False)
    status_order = serializers.IntegerField(required=False, allow_null=True)
    item_in_package = serializers.BooleanField(required=False)
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "flavour_level",
            "product",
            "topping",
            "package",
            "consignment",
            'package',
            "size",
            "total_price",
            'price_item',
            "description",
            "amount",
            "product_set",
            "topping_set",
            "package_set",
            "orderitemtopping_set",
            "order",
            "code",
            'status_order',
            'item_in_package'
        ]
        read_only_fields = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    payment_id = serializers.IntegerField(required=True, allow_null=True)
    address_id = serializers.IntegerField(required=True, allow_null=True)
    customer_id = serializers.IntegerField(required=False, allow_null=True)
    sale_channel_id = serializers.IntegerField(required=False, allow_null=True)
    voucher_id = serializers.IntegerField(required=False, allow_null=True)
    point_promotion_id = serializers.IntegerField(required=False, allow_null=True)

    sale_channel_set = GetterSaleChannel(
        read_only=True, source="sale_channel")
    payment_set = PaymentSerializer(read_only=True, source="payment")
    address_set = AddressCustomerSerializer(read_only=True, source="address")
    orderitem_set = OrderItemSerializer(many=True)
    customer_set = CustomerSerializer(read_only=True, source='customer')

    status_order = serializers.IntegerField(required=False, allow_null=True)
    status_food = serializers.IntegerField(required=False, allow_null=True)
    status_drink = serializers.IntegerField(required=False, allow_null=True)
    create_at = serializers.DateTimeField(required=False, allow_null=True) 
    point = serializers.IntegerField(required=False, allow_null=True)
    change = serializers.IntegerField(required=False, allow_null=True)
    cash = serializers.IntegerField(required=False, allow_null=True)
    reason = serializers.CharField(required=False, allow_blank=True)
    table = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [                   
            "sale_channel_set",
            "orderitem_set",
            'payment_set',
            "address_set",
            "customer_set",
            "reason",
            "sale_channel_id",
            "customer_id",
            "payment_id",
            "address_id",
            "id",
            "table",
            "order_number",
            "total_balance",
            "discount",
            "discount_percent",
            "status_delivery",
            "status_food",
            "status_drink",
            "total_price",
            "total_amount",
            "description",
            "status_order",
            "payment_status",
            "create_by",
            "update_by",
            'delivery_price',
            "create_at",
            "update_at",
            "voucher_id",
            "point_promotion_id",
            "point",
            "cash",
            "change",
        ]

    def create(self, validated_data):
        orderitem_set = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        for item in orderitem_set:
            have_topping = False
            if 'orderitemtopping_set' in item:
                orderitemtopping_set = item.pop('orderitemtopping_set')
                if not orderitemtopping_set == []:
                    have_topping = True
                print(orderitemtopping_set)
            order_item = OrderItem.objects.create(**item, order=order)
            if have_topping:
                for topping in orderitemtopping_set:
                    OrderItemTopping.objects.create(**topping, item=order_item)
        return order

    def update(self, instance, validated_data):
        instance.customer_id = validated_data['customer_id']
        instance.table = validated_data['table']
        instance.order_number = validated_data['order_number']
        instance.total_balance = validated_data['total_balance']
        instance.discount = validated_data['discount']
        instance.discount_percent = validated_data['discount_percent']
        instance.status_delivery = validated_data['status_delivery']
        instance.status_food = validated_data['status_food']
        instance.status_drink = validated_data['status_drink']
        instance.total_price = validated_data['total_price']
        instance.total_amount = validated_data['total_amount']
        instance.sale_channel_id = validated_data['sale_channel_id']
        instance.description = validated_data['description']
        instance.status_order = validated_data['status_order']
        instance.payment_id = validated_data['payment_id']
        instance.payment_status = validated_data['payment_status']
        instance.update_by = validated_data['update_by']
        instance.delivery_price = validated_data['delivery_price']
        instance.update_at = datetime.datetime.now()
        instance.address_id = validated_data['address_id']
        instance.cash = validated_data['cash']
        instance.change = validated_data['change']
        instance.reason = validated_data['reason']
        instance.save()
        orderitem_id = [c['id'] for c in validated_data['orderitem_set'] if c.get('id')]
        
        OrderItem.objects.filter(order_id=instance.id).exclude(
            id__in=orderitem_id).delete()

        to_be_create = [c for c in validated_data['orderitem_set'] if c.get("id") == None]
        for i in to_be_create:
            if 'orderitemtopping_set' in i:
                orderitemtopping_set = i.pop('orderitemtopping_set')
            item = OrderItem.objects.create(order_id=instance.id, **i)
            if 'orderitemtopping_set' in i:
                for p in i['orderitemtopping_set']:
                    OrderItemTopping.objects.create(**p, item_id=item.id)

        to_be_update = [c for c in validated_data['orderitem_set'] if c.get('id')]
        for i in to_be_update:
            if 'orderitemtopping_set' in i:
              orderitemtopping_set = i.pop('orderitemtopping_set')
            OrderItem.objects.filter(id=i['id']).update(
                order_id=instance.id, **i)
            if 'orderitemtopping_set' in i:
                to_be_create_topping = [
                    c for c in orderitemtopping_set if c.get("id")]
                for p in to_be_create_topping:
                    OrderItemTopping.objects.create(**p)

            to_be_delete_topping = [c['id'] for c in orderitemtopping_set]
            for p in to_be_delete_topping:
                OrderItemTopping.objects.filter(item_id=i['id']).exclude(
                    id__in=to_be_delete_topping).delete()

            to_be_update_topping = [c for c in orderitemtopping_set]
            for p in to_be_update_topping:
                OrderItemTopping.objects.filter(item_id=p['id']).update(**p)
        return instance
