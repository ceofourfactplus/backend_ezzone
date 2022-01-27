import os
from django.db.models import Sum, F, Count
from product.models import SaleChannel
from pos.models import Order, OrderItem, OrderItemTopping, Payment
from pos.serializers import OrderSerializer, PaymentSerializer, OrderItemSerializer, OrderItemToppingSerializer
from rest_framework.views import APIView
from customer.models import Customer, AddressCustomer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from pprint import pprint
from product.models import Product, SaleChannel, Topping
from product.serializers import ProductReportSerialiser, ChannelReportSerializer
from datetime import datetime
from promotion.models import PackageItem, PromotionPackage,CustomerPoint


class cancel_order(APIView):
    def put(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status_order = 4
        order.save()
        return Response('ok')


def check_is_finish(order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise 404

    print('status food:', order.status_food)
    print('status drink:', order.status_drink)
    print('status order:', order.status_order)
    # for food
    product_food = Product.objects.filter(type_product__in=[1, 3])
    product_food_id = [p.id for p in product_food]
    order_food_item = OrderItem.objects.filter(
        product_id__in=product_food_id, order_id=order_id)
    arr_status_food = [s.status_order for s in order_food_item]
    no_none_status_food_list = [s for s in arr_status_food if s != None]

    topping_food = Topping.objects.filter(type_topping__in=[1, 3])
    topping_food_id = [p.id for p in topping_food]
    order_food_topping = OrderItem.objects.filter(
        topping_id__in=topping_food_id, order_id=order_id)
    print([i.status_order for i in order_food_topping])
    arr_status_top_food = [s.status_order for s in order_food_topping]
    no_none_status_top_food_list = [
        s for s in arr_status_top_food if s != None]

    if not (no_none_status_food_list + no_none_status_top_food_list) == []:
        order.status_food = min(
            no_none_status_food_list + no_none_status_top_food_list)
    else:
        order.status_food = None

    # for drink
    product_drink = Product.objects.filter(type_product__in=[2])
    product_drink_id = [p.id for p in product_drink]
    order_drink_item = OrderItem.objects.filter(
        product_id__in=product_drink_id, order_id=order_id)
    arr_status_drink = [s.status_order for s in order_drink_item]
    no_none_status_drink_list = [s for s in arr_status_drink if s != None]

    topping_drink = Topping.objects.filter(type_topping__in=[2])
    topping_drink_id = [p.id for p in topping_drink]
    order_drink_topping = OrderItem.objects.filter(
        topping_id__in=topping_drink_id, order_id=order_id)
    arr_status_top_drink = [s.status_order for s in order_drink_topping]
    no_none_status_top_drink_list = [
        s for s in arr_status_top_drink if s != None]

    
    if not (no_none_status_drink_list + no_none_status_top_drink_list) == []:
        order.status_drink = min(
            no_none_status_drink_list + no_none_status_top_drink_list)
    else:
        order.status_drink = None

    if not order.status_drink == None and not order.status_food == None:
        if order.status_drink > order.status_food:
            order.status_order = order.status_food
        if order.status_drink < order.status_food:
            order.status_order = order.status_drink

    if (order.status_drink == 1) and (order.status_food == 1 or order.status_food == None):
        order.status_order = 1
    if (order.status_drink == 2 or order.status_drink == None) and (order.status_food == 2 or order.status_food == None):
        order.status_order = 2
    print('payment status is :',order.payment_status)
    print('check is :',(order.status_drink == 3 or order.status_drink == None) and (order.status_food == 3 or order.status_food == None) and (order.payment_status == 3 or order.payment_status == 4))
    if (order.status_drink == 3 or order.status_drink == None) and (order.status_food == 3 or order.status_food == None) and (order.payment_status == 3 or order.payment_status == 4):
        order.status_order = 3
    if (order.status_drink == 4 or order.status_drink == None) and (order.status_food == 4 or order.status_food == None):
        order.status_order = 4
    # if order.status_drink > order.status_food:
    #     order.status_order = order.status_food
    # else: order.status_order = order.status_drink

    order.spen_time = str(
        datetime.now() - order.create_at.replace(tzinfo=None))

    order.save()


class ChangeStatusOrder(APIView):
    def put(self,  request, where, all_order, status, pk):
        # get type
        if where == 'kitchen':
            type_item = [1, 3]
            order_status = 'order_food'
        elif where == 'counter':
            order_status = 'order_drink'
            type_item = [2]

        # get table
        if all_order:
            order = Order.objects.get(pk=pk)
            if where == 'kitchen':
                order.status_food = status
            elif where == 'counter':
                order.status_drink = status
            order.save()

            product = [p.id for p in Product.objects.filter(
                type_product__in=type_item)]
            orderitem = OrderItem.objects.filter(
                order_id=pk, product_id__in=product)
            for item in orderitem:
                item.status_order = status
                item.save()

            topping = [p.id for p in Topping.objects.filter(
                type_topping__in=type_item)]
            orderitem_top = OrderItem.objects.filter(
                order_id=pk, topping_id__in=topping)
        
            for item in orderitem_top:
                item.status_order = status
                item.save()

            check_is_finish(pk)
        else:
            orderitem = OrderItem.objects.get(pk=pk)
            orderitem.status_order = status
            orderitem.save()

            check_is_finish(orderitem.order_id)
        return Response('ok')


class ServeOrderItem(APIView):
    def put(self, request, pk):
        orderitem = OrderItem.objects.get(pk=pk)
        orderitem.status_order = 3
        orderitem.save()


class SelectPaymentOrder(APIView):

    def put(self, request, order_id, payment_id):
        orders = Order.objects.get(pk=order_id)
        orders.payment_status = 4
        payment = Payment.objects.get(pk=payment_id)
        if payment.payment.upper() == "CASH":
            orders.payment_status = 3
            orders.cash = request.data['cash']
            orders.change = int(float(orders.total_balance)
                                ) - int(request.data['cash'])
        orders.payment_id = payment_id
        orders.save()
        check_is_finish(order_id)
        return Response('ok')


class PaymentDetail(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def delete(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        if not payment.img == None:
            payment.img.delete(save=True)
        payment.delete()
        return Response('ok')

    def put(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        if not request.data['img'] == None:
            payment.img.delete(save=True)
        serializer = PaymentSerializer(payment, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('ok')
        return Response(serializer.errors, status=400)


class PaymentList(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        payments = Payment.objects.all()
        for payment in payments:
            if Order.objects.filter(payment_id=payment.id).exists():
                payment.is_used = True
            else:
                payment.is_used = False
        serializer = PaymentSerializer(
            payments, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TodayOrderList(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date())
        serializer = OrderSerializer(
            Orders, context={'request': request}, many=True)
        return Response(serializer.data)

# do order


class DrinkOrderOnGoing(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_drink__in=[0, 1]).exclude(status_drink=None)
        serializer = OrderSerializer(
            Orders, context={'request': request}, many=True)
        return Response(serializer.data)


# read order

class CounterOrderType(APIView):
    def get(self, request, type):
        if type == 5:
            order_food = Order.objects.filter(
                create_at__gte=datetime.now().date()).exclude(status_drink=None).order_by('-create_at')
        elif type == 4:
            order_food = Order.objects.filter(create_at__gte=datetime.now().date(
            ), status_order=type).exclude(status_drink=None).order_by('-create_at')
        elif type == 3:
            order_food = Order.objects.filter(create_at__gte=datetime.now().date(
            ), status_drink=type).exclude(status_order=4).order_by('-create_at')
        serializer = OrderSerializer(
            order_food, context={'request': request}, many=True)
        return Response(serializer.data, status=200)


class CounterOrderToday(APIView):
    def get(self, request):
        data = {}
        data['finish_order'] = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_drink=2).exclude(status_order=4).count()
        data['remain_order'] = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_drink=1).exclude(status_order=4).count()
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_drink__in=[0, 1, 2]).exclude(status_order=4)
        data['order'] = OrderSerializer(Orders, many=True).data
        return Response(data, status=200)


class KitchenOrderType(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, type):
        if type == 5:
            order_food = Order.objects.filter(
                create_at__gte=datetime.now().date()).exclude(status_food=None).order_by('-create_at')
        elif type == 4:
            order_food = Order.objects.filter(create_at__gte=datetime.now().date(
            ), status_order=type).exclude(status_food=None).order_by('-create_at')
        elif type == 3:
            order_food = Order.objects.filter(create_at__gte=datetime.now().date(
            ), status_food=type).exclude(status_order=4).order_by('-create_at')
        serializer = OrderSerializer(
            order_food, context={'request': request}, many=True)
        return Response(serializer.data, status=200)


class KitchenOrderToday(APIView):
    def get(self, request):
        data = {}
        data['finish_order'] = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_food=3).count()
        data['remain_order'] = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_food=1).count()
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_food__in=[0, 1, 2]).exclude(status_order=4)
        data['order'] = OrderSerializer(Orders, many=True).data
        return Response(data, status=200)


class TodayOrderCompleted(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_order=3)
        serializer = OrderSerializer(
            Orders, context={'request': request}, many=True)
        return Response(serializer.data)


class TodayOrderUnpaid(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date(), payment_status__in=[1, 2]).exclude(status_order=4)  # get not pay today order don`t want cancel order
        serializer = OrderSerializer(
            Orders, context={'request': request}, many=True)
        return Response(serializer.data)


class TodayOrderOnGoing(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_order__in=[0, 1, 2])
        serializer = OrderSerializer(
            Orders, context={'request': request}, many=True)
        return Response(serializer.data)


class TodayOrderVoid(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        Orders = Order.objects.filter(
            create_at__gte=datetime.now().date(), status_order=4)
        serializer = OrderSerializer(
            Orders, context={'request': request}, many=True)
        return Response(serializer.data)


class OrderList(APIView):
    def get(self, request):
        Orders = Order.objects.all()
        serializer = OrderSerializer(Orders, many=True)
        return Response(serializer.data)

    def post(self, request):

        order = Order.objects.filter(
            create_at__gte=datetime.now().date())
        amount_order = len(order)+1
        request.data['order_number'] = amount_order

        # check customer
        if request.data['phone_number'] == "":
            request.data['customer_id'] = None
            request.data['address_id'] = None
        else:  # check is has customer in data
            if Customer.objects.filter(phone_number=request.data['phone_number']).exists():
                request.data['customer_id'] = Customer.objects.get(
                    phone_number=request.data['phone_number']).id
                if not(request.data['point_promotion_id'] == None ):
                    if CustomerPoint.objects.filter(customer_id=request.data['customer_id'],point_promotion_id=request.data['point_promotion_id']).exists():
                        cus_point = CustomerPoint.objects.get(customer_id=request.data['customer_id'],point_promotion_id=request.data['point_promotion_id'])
                        cus_point.point += request.data['point']
                        print('customer point 666')
                        cus_point.save()
                    else:
                        print('customer point')
                        CustomerPoint.objects.create(customer_id=request.data['customer_id'],point_promotion_id=request.data['point_promotion_id'],point = request.data['point'])
                        
                # check address
                if not request.data['address'] == "":
                    if AddressCustomer.objects.filter(customer_id=request.data['customer_id'], address=request.data['address']).exists():
                        request.data['address_id'] = AddressCustomer.objects.get(
                            address=request.data['address'], customer_id=request.data['customer_id']).id
                    else:
                        request.data['address_id'] = AddressCustomer.objects.create(
                            address=request.data['address'], customer_id=request.data['customer_id']).id
                else:
                    request.data['address_id'] = None
            else:
                request.data['customer_id'] = Customer.objects.create(
                    phone_number=request.data['phone_number'], nick_name=request.data['nick_name']).id
                
                if not(request.data['point_promotion_id'] == None ):
                    CustomerPoint.objects.create(customer_id=request.data['customer_id'],point_promotion_id=request.data['point_promotion_id'],point = request.data['point'])
                if not request.data['address'] == "":
                    request.data['address_id'] = AddressCustomer.objects.create(
                        address=request.data['address'], customer_id=request.data['customer_id']).id
                else:
                    request.data['address_id'] = None

        # check status order
        request.data['status_food'] = None
        request.data['status_drink'] = None

        product = [item['product_set']['type_product']
                   for item in request.data['orderitem_set'] if 'product_set' in item]
        topping = [item['topping_set']['type_topping']
                   for item in request.data['orderitem_set'] if 'topping' in item]
        package = [item['package']
                   for item in request.data['orderitem_set'] if 'package' in item]

        food = [p.id for p in Product.objects.filter(type_product__in=[1, 3])]
        drink = [p.id for p in Product.objects.filter(type_product__in=[2])]
        for p in package:
            if PackageItem.objects.filter(package=p, product__in=food).exists():
                request.data['status_food'] = 0
            if PackageItem.objects.filter(package=p, product__in=drink).exists():
                request.data['status_drink'] = 0
        for n in product:
            if n == 3 or n == 1:
                request.data['status_food'] = 0
            if n == 2:
                request.data['status_drink'] = 0

        for n in topping:
            if n == 3 or n == 1:
                request.data['status_food'] = 0
            if n == 2:
                request.data['status_drink'] = 0

        for item in request.data['orderitem_set']:
            if 'package' in item:
                for i in item['package_set']['packageitem_set']:
                    
                    data = {
                        "code": i['product_set']['name'],
                        "flavour_level": 2,
                        "product": i['product'],
                        "price_item": 0,
                        "total_price": 0,
                        "size": "M",
                        "description": "",
                        "amount": i['qty'],
                        'item_in_package':True,
                        'orderitemtopping_set':[]
                        } 
                    for t in i['itemtopping_set']:
                        data['orderitemtopping_set'].append({
                            'topping':t['topping'],    
                            'price_topping':0,
                            "total_price":0,
                            "amount":t['qty']
                        })
                    request.data['orderitem_set'].append(data)
                print(request.data['orderitem_set'])
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class OrderDetail(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise 404

    def get(self, request, pk):
        Order = self.get_object(pk)
        serializer = OrderSerializer(Order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(';ldkfja;lkfjas;dfknaz;ldkna;dlvn;j n.dkhfljdlrlvj')
            check_is_finish(pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        Order = self.get_object(pk)
        Order.delete()
        return Response(status=204)


class OrderItemList(APIView):
    def get(self, request):
        Orders = OrderItem.objects.all()
        serializer = OrderItemSerializer(Orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrderItemDetail(APIView):
    def get_object(self, pk):
        try:
            return OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            raise 404

    def get(self, request, pk):
        Order = self.get_object(pk)
        serializer = OrderItemSerializer(Order)
        return Response(serializer.data)

    def put(self, request, pk):
        Order = self.get_object(pk)
        serializer = OrderItemSerializer(Order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        Order = self.get_object(pk)
        Order.delete()
        return Response(status=204)


class OrderItemToppingList(APIView):
    def get(self, request):
        Orders = OrderItemTopping.objects.all()
        serializer = OrderItemToppingSerializer(Orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderItemToppingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrderItemToppingDetail(APIView):
    def get_object(self, pk):
        try:
            return OrderItemTopping.objects.get(pk=pk)
        except OrderItemTopping.DoesNotExist:
            raise 404

    def get(self, request, pk):
        Order = self.get_object(pk)
        serializer = OrderItemToppingSerializer(Order)
        return Response(serializer.data)

    def put(self, request, pk):
        Order = self.get_object(pk)
        serializer = OrderItemToppingSerializer(Order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        Order = self.get_object(pk)
        Order.delete()
        return Response(status=204)


class AllOrder(APIView):
    def post(self, request):
        # order_before = request.data
        # order_before['']
        # order = OrderSerializer(data=request.data)
        # if order.is_valid():
        #     order.save()
        #     for product in request.data['cart']:
        #         product['order'] = order.data['id']
        #         product['product_id'] = product['product']['id']
        #         product_serializer = OrderItemSerializer(data=product)
        #         if product_serializer.is_valid():
        #             product_serializer.save()
        #             for topping in product['topping']:
        #                 topping['item'] = product_serializer.data['id']
        #                 topping['topping_id']  = topping['topping']['id']
        #                 topping_serializer = OrderItemToppingSerializer(data=topping)
        #                 if topping_serializer.is_valid:
        #                     topping_serializer.save()
        #                     return Response(order.data, status=201)
        #                 return Response(topping_serializer.errors,status=400)
        #         return Response(product_serializer.errors,status=400)
        # return Response(order.errors,status=400)
        return Response('ok')


class Report (APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        order = Order.objects.all()
        report = order.aggregate(Sum('total_balance'), Sum('discount'))
        report['total_order'] = order.count()
        report['total_cash'] = order.filter(
            payment_status=3).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_transfer'] = order.filter(
            payment_status=4).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_customer'] = order.filter(
            customer_id__isnull=False).values('customer_id').distinct().count()
        all_channel_id = [channel.id for channel in SaleChannel.objects.all()]
        total_price = []
        for channel_id in all_channel_id:
            total_balance = order.filter(sale_channel_id=channel_id).aggregate(
                Sum('total_balance'))['total_balance__sum']
            total_price.append({
                'total_price': total_balance,
                'sale_channel_set': ChannelReportSerializer(SaleChannel.objects.get(id=channel_id), context={'request': request}).data,
            })
        report['sale_channel_total_price'] = total_price
        # find top food
        filter_food = [
            product.id for product in Product.objects.filter(type_product=3)]
        all_food = OrderItem.objects.filter(product_id__in=filter_food)
        top_food = all_food.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_food = [t['product_id'] for t in top_food]
        top_product_data = Product.objects.filter(id__in=list_food)
        report['top_food'] = ProductReportSerialiser(
            top_product_data, many=True).data

        # find top drink
        filter_drink = [
            product.id for product in Product.objects.filter(type_product=2)]
        all_drink = OrderItem.objects.filter(product_id__in=filter_drink,)
        top_drink = all_drink.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_drink = [t['product_id'] for t in top_drink]
        top_drink_data = Product.objects.filter(id__in=list_drink)
        report['top_drink'] = ProductReportSerialiser(
            top_drink_data, many=True).data

        # find top dressert
        filter_dressert = [
            product.id for product in Product.objects.filter(type_product=1)]
        all_dressert = OrderItem.objects.filter(
            product_id__in=filter_dressert,)
        top_dressert = all_dressert.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_dressert = [t['product_id'] for t in top_dressert]
        top_dressert_data = Product.objects.filter(id__in=list_dressert)
        report['top_dressert'] = ProductReportSerialiser(
            top_dressert_data, many=True).data

        return Response(report, status=200)


class ReportDaily (APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        order = Order.objects.filter(
            create_at__gte=datetime.now().date())
        order_id_list = [item.id for item in order]
        report = order.aggregate(Sum('total_balance'), Sum('discount'))
        report['total_order'] = order.count()
        report['total_cash'] = order.filter(
            payment_status=3).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_transfer'] = order.filter(
            payment_status=4).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_customer'] = order.filter(
            customer_id__isnull=False).values('customer_id').distinct().count()
        all_channel_id = [channel.id for channel in SaleChannel.objects.all()]
        total_price = []
        for channel_id in all_channel_id:
            total_balance = order.filter(sale_channel_id=channel_id).aggregate(
                Sum('total_balance'))['total_balance__sum']
            total_price.append({
                'total_price': total_balance,
                'sale_channel_set': ChannelReportSerializer(SaleChannel.objects.get(id=channel_id), context={'request': request}).data,
            })
        report['sale_channel_total_price'] = total_price
        # find top food
        filter_food = [
            product.id for product in Product.objects.filter(type_product=3)]
        all_food = OrderItem.objects.filter(
            product_id__in=filter_food, order_id__in=order_id_list)
        top_food = all_food.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_food = [t['product_id'] for t in top_food]
        top_product_data = Product.objects.filter(id__in=list_food)
        report['top_food'] = ProductReportSerialiser(
            top_product_data, many=True).data

        # find top drink
        filter_drink = [
            product.id for product in Product.objects.filter(type_product=2)]
        all_drink = OrderItem.objects.filter(
            product_id__in=filter_drink, order_id__in=order_id_list)
        top_drink = all_drink.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_drink = [t['product_id'] for t in top_drink]
        top_drink_data = Product.objects.filter(id__in=list_drink)
        report['top_drink'] = ProductReportSerialiser(
            top_drink_data, many=True).data

        # find top dressert
        filter_dressert = [
            product.id for product in Product.objects.filter(type_product=1)]
        all_dressert = OrderItem.objects.filter(
            product_id__in=filter_dressert, order_id__in=order_id_list)
        top_dressert = all_dressert.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_dressert = [t['product_id'] for t in top_dressert]
        top_dressert_data = Product.objects.filter(id__in=list_dressert)
        report['top_dressert'] = ProductReportSerialiser(
            top_dressert_data, many=True).data

        return Response(report, status=200)


class ReportFilterByDate (APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, year, month, date):
        order = Order.objects.filter(
            create_at__gte=datetime(year, month, date))
        order_id_list = [item.id for item in order]
        report = order.aggregate(Sum('total_balance'), Sum('discount'))
        report['total_order'] = order.count()
        report['total_cash'] = order.filter(
            payment_status=3).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_transfer'] = order.filter(
            payment_status=4).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_customer'] = order.filter(
            customer_id__isnull=False).values('customer_id').distinct().count()
        all_channel_id = [channel.id for channel in SaleChannel.objects.all()]
        total_price = []
        for channel_id in all_channel_id:
            total_balance = order.filter(sale_channel_id=channel_id).aggregate(
                Sum('total_balance'))['total_balance__sum']
            total_price.append({
                'total_price': total_balance,
                'sale_channel_set': ChannelReportSerializer(SaleChannel.objects.get(id=channel_id), context={'request': request}).data,
            })
        report['sale_channel_total_price'] = total_price
        # find top food
        filter_food = [
            product.id for product in Product.objects.filter(type_product=3)]
        all_food = OrderItem.objects.filter(
            product_id__in=filter_food, order_id__in=order_id_list)
        top_food = all_food.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_food = [t['product_id'] for t in top_food]
        top_product_data = Product.objects.filter(id__in=list_food)
        report['top_food'] = ProductReportSerialiser(
            top_product_data, many=True).data

        # find top drink
        filter_drink = [
            product.id for product in Product.objects.filter(type_product=2)]
        all_drink = OrderItem.objects.filter(
            product_id__in=filter_drink, order_id__in=order_id_list)
        top_drink = all_drink.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_drink = [t['product_id'] for t in top_drink]
        top_drink_data = Product.objects.filter(id__in=list_drink)
        report['top_drink'] = ProductReportSerialiser(
            top_drink_data, many=True).data

        # find top dressert
        filter_dressert = [
            product.id for product in Product.objects.filter(type_product=1)]
        all_dressert = OrderItem.objects.filter(
            product_id__in=filter_dressert, order_id__in=order_id_list)
        top_dressert = all_dressert.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_dressert = [t['product_id'] for t in top_dressert]
        top_dressert_data = Product.objects.filter(id__in=list_dressert)
        report['top_dressert'] = ProductReportSerialiser(
            top_dressert_data, many=True).data

        return Response(report, status=200)


class ReportMonth (APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        now = datetime.now()
        order = Order.objects.filter(
            create_at__gte=datetime(now.year, now.month, 1))
        order_id_list = [item.id for item in order]
        report = order.aggregate(Sum('total_balance'), Sum('discount'))
        report['total_order'] = order.count()
        report['total_cash'] = order.filter(
            payment_status=3).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_transfer'] = order.filter(
            payment_status=4).aggregate(Sum('total_balance'))['total_balance__sum']
        report['total_customer'] = order.filter(
            customer_id__isnull=False).values('customer_id').distinct().count()
        all_channel_id = [channel.id for channel in SaleChannel.objects.all()]
        total_price = []
        for channel_id in all_channel_id:
            total_balance = order.filter(sale_channel_id=channel_id).aggregate(
                Sum('total_balance'))['total_balance__sum']
            total_price.append({
                'total_price': total_balance,
                'sale_channel_set': ChannelReportSerializer(SaleChannel.objects.get(id=channel_id), context={'request': request}).data,
            })
        report['sale_channel_total_price'] = total_price
        # find top food
        filter_food = [
            product.id for product in Product.objects.filter(type_product=3)]
        all_food = OrderItem.objects.filter(
            product_id__in=filter_food, order_id__in=order_id_list)
        top_food = all_food.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_food = [t['product_id'] for t in top_food]
        top_product_data = Product.objects.filter(id__in=list_food)
        report['top_food'] = ProductReportSerialiser(
            top_product_data, many=True).data

        # find top drink
        filter_drink = [
            product.id for product in Product.objects.filter(type_product=2)]
        all_drink = OrderItem.objects.filter(
            product_id__in=filter_drink, order_id__in=order_id_list)
        top_drink = all_drink.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_drink = [t['product_id'] for t in top_drink]
        top_drink_data = Product.objects.filter(id__in=list_drink)
        report['top_drink'] = ProductReportSerialiser(
            top_drink_data, many=True).data

        # find top dressert
        filter_dressert = [
            product.id for product in Product.objects.filter(type_product=1)]
        all_dressert = OrderItem.objects.filter(
            product_id__in=filter_dressert, order_id__in=order_id_list)
        top_dressert = all_dressert.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:3]
        list_dressert = [t['product_id'] for t in top_dressert]
        top_dressert_data = Product.objects.filter(id__in=list_dressert)
        report['top_dressert'] = ProductReportSerialiser(
            top_dressert_data, many=True).data

        return Response(report, status=200)


class ReportAllProduct (APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        now = datetime.now()
        # order = Order.objects.filter(
        #     create_at__gte=datetime(now.year,now.month,1))
        order = Order.objects.all()
        order_id_list = [item.id for item in order]
        report = {}

        # find top 10 food and total_price_drink

        filter_food = [
            product.id for product in Product.objects.filter(type_product=3)]
        all_food = OrderItem.objects.filter(
            product_id__in=filter_food, order_id__in=order_id_list)
        top_food = all_food.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:10]
        list_food = [t['product_id'] for t in top_food]
        top_product_data = Product.objects.filter(id__in=list_food)
        report['top_food'] = ProductReportSerialiser(
            top_product_data, context={'request': request}, many=True).data
        report['total_price_food'] = all_food.aggregate(
            Sum('total_price'))['total_price__sum']

        # find top 10 drink and total_sale_drink
        filter_drink = [
            product.id for product in Product.objects.filter(type_product=2)]
        all_drink = OrderItem.objects.filter(
            product_id__in=filter_drink, order_id__in=order_id_list)
        top_drink = all_drink.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:10]
        list_drink = [t['product_id'] for t in top_drink]
        top_drink_data = Product.objects.filter(id__in=list_drink)
        report['top_drink'] = ProductReportSerialiser(
            top_drink_data, context={'request': request}, many=True).data
        report['total_price_drink'] = all_drink.aggregate(Sum('total_price'))[
            'total_price__sum']

        # find top dressert
        filter_dressert = [
            product.id for product in Product.objects.filter(type_product=1)]
        all_dressert = OrderItem.objects.filter(
            product_id__in=filter_dressert, order_id__in=order_id_list)
        top_dressert = all_dressert.annotate(frequency=Count('product_id')).order_by(
            'frequency').values('product_id').distinct()[:10]
        list_dressert = [t['product_id'] for t in top_dressert]
        top_dressert_data = Product.objects.filter(id__in=list_dressert)
        report['top_dressert'] = ProductReportSerialiser(
            top_dressert_data, context={'request': request}, many=True).data
        report['total_price_dressert'] = all_dressert.aggregate(Sum('total_price'))[
            'total_price__sum']

        return Response(report, status=200)


class GetOrderNumber(APIView):
    def get(self, request):
        order = Order.objects.filter(
            create_at__gte=datetime.now().date())
        amount_order = len(order)
        print(amount_order+1)
        return Response({'order_number': amount_order+1})


class delete_all_order(APIView):
    def delete(self, request):
        Order.objects.all().delete()
        Customer.objects.all().delete()
        return Response('oj')

