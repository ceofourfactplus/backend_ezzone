from django.db.models import fields
from rest_framework import serializers
from .models import User,Login


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'is_superuser',
            'username',
            'nick_name', 
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined', 
            'is_chef', 
            'is_barista', 
            'is_purchesing', 
            'is_receptionist', 
            'is_owner', 
            'id_card',
            'birth_date', 
            'is_working', 
            'gender', 
            'img',
        ]
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    user_set = UserSerializer(read_only=True,source="user")
    class Meta:
        model = Login
        fields = ['id','token','user','login_at','logout_at','time_login','user_set'] 