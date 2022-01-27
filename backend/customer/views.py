from turtle import st
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from customer.serializers import CustomerSerializer, CustomerImageSerializer
from customer.models import Customer, AddressCustomer
import datetime
from django.db.models import F, Value
from rest_framework.parsers import FormParser, MultiPartParser
from pos.models import Order, OrderItem, OrderItemTopping
from product.models import Product
from product.serializers import ProductS

# Create your views here.


class GetCustomerByPhoneNumbe(APIView):
    def get(self, request, phone_number):
        customer = Customer.objects.filter(phone_number__contains=phone_number)
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data, status=200)

class CheckPhoneNumber(APIView):
    def get(self, request, phone_number):
        if Customer.objects.filter(phone_number=phone_number).exists():
            return Response('Phone number ' + phone_number + ' is already in use',status=400)
        return Response('don`t have a valid phone number',status=200)

class CheckPhoneNumberEdit(APIView):
    def get(self, request, phone_number,pk):
        if Customer.objects.filter(phone_number=phone_number).exclude(pk=pk).exists():
            return Response('Phone number ' + phone_number + ' is already in use',status=400)
        return Response('don`t have a valid phone number',status=200)

class CustomerList (APIView):

    def get(self, request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(
            customer, context={'request': request}, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        if not request.data['invited_by'] == None:
            request.data['invited_by'] = int(request.data['invited_by'])
        if Customer.objects.filter(phone_number=request.data['phone_number']):
            return Response('Phone number is already taken.', status=400)
        else:      
            serializer = CustomerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data['id'])
            if 'addresscustomer_set' in request.data:
                AddressCustomer.objects.create(
                    address=request.data['addresscustomer_set']['address'],
                    customer_id=serializer.data['id'],
                    status_address=1,
                )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CustomerImage(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise 404

    def put(self, request, pk):
        customer = self.get_object(pk)
        print(request.data)
        serializer = CustomerImageSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

from django.db.models import Avg, Count, Min, Sum
from promotion.models import CustomerPoint,PointPromotion

class GetCustomer(APIView):

    parser_classes = [MultiPartParser, FormParser]
    
    def get_favorite_menu(self, pk):
        orders_id = [order.id for order in Order.objects.filter(customer_id=pk)]
        order_items = OrderItem.objects.filter(order_id__in=orders_id)
        products = {}
        for i in order_items:
            if not products.get(i.product_id):
                products[i.product_id] = i.amount
            else:
                products[i.product_id] += i.amount
        products = dict(sorted(products.items(), key=lambda item: item[1], reverse=True))
        top_products = []
        for i in products.keys():
            product = Product.objects.get(id=i)
            serializer = ProductS(product)
            top_products.append(serializer.data)
            
        return top_products[:3]

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise 404

    def get(self, request, pk):
        data = {}
        if PointPromotion.objects.filter(status=True).exists():
            if CustomerPoint.objects.filter(customer_id=pk,point_promotion_id=PointPromotion.objects.get(status=True)).exists():
                data['point'] = CustomerPoint.objects.get(customer_id=pk,point_promotion_id=PointPromotion.objects.get(status=True)).point
            else:
                data['point'] = 0   
            data['total_promotion'] = Order.objects.filter(customer_id=pk,point_promotion_id=PointPromotion.objects.get(status=True)).aggregate(Sum('total_balance'))['total_balance__sum']
        else:
            data['point'] = 0
            data['total_promotion'] = 0 
        orders = [order for order in Order.objects.filter(customer_id=pk)]
        customer = self.get_object(pk)
        data['customer'] = CustomerSerializer(customer, context={"request": request}).data
        if len(orders) != 0:
            data['customer']['date_joined'] = orders[0].create_at
            data['customer']['last_joined'] = orders[-1].create_at
        else:
            data['customer']['date_joined'] = 'xxxx-xx-xx'
            data['customer']['last_joined'] = 'xxxx-xx-xx'
        data['total_price'] = Order.objects.filter(customer_id=pk).aggregate(Sum('total_balance'))['total_balance__sum']
        data['top_products'] = self.get_favorite_menu(pk)
        return Response(data, status=200)


class CustomerDetail(APIView):

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise 404

    def put(self, request, pk):
        customer = self.get_object(pk)
        if not request.data['invited_by'] == None:
            request.data['invited_by'] = int(request.data['invited_by'])
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SaveAddress(APIView):

    def put(self, request, pk):
        if 'id' in request.data:
            customer = AddressCustomer.objects.get(pk=request.data['id'])
            customer.address = request.data['address']
            customer.save()
        else:
            AddressCustomer.objects.create(
                address=request.data['address'],
                customer_id=request.data['customer'],
                status_address=1,
            ) 
        print(customer.address)
        return Response('ok')


class CreateAddress(APIView):
    def post(self, request):
        AddressCustomer.objects.create(
            address=request.data['address'],
            customer_id=request.data['customer_id'],
            status_address=1,
        )
        return Response('ok')


class SearchName (APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, text):
        customer = Customer.objects.filter(nick_name__contains=text)
        serializer = CustomerSerializer(
            customer, context={"request": request}, many=True)
        return Response(serializer.data, status=200)
