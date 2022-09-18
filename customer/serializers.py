from django.db.models import fields
from customer.models import Customer, AddressCustomer
from rest_framework import serializers


class AddressCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressCustomer
        fields = '__all__'


class CustomerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'img']


class CustomerSerializer(serializers.ModelSerializer):
       class Meta:
        model = Customer
        fields = '__all__'

    invited_by = DynamicRelationField('CustomerSerializer', embed=True) 