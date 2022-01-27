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
    addresscustomer_set = AddressCustomerSerializer(many=True, read_only=True)
    email = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    img = serializers.ImageField(read_only=True)
    invited_by = serializers.PrimaryKeyRelatedField(allow_null=True,queryset=Customer.objects.all())
    last_name = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Customer
        fields = [
            'id',
            'nick_name',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'img', 'email',
            'addresscustomer_set',
            'birth_date',
            'line_customer_id',
            'invited_by',
            'date_joined',
            'last_joined'
        ]
