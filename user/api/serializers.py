from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..user_model.user import User
from ..models import ( CustomerProfile, VendorProfile )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ( 'id', 'email', 'phone_number', 'password', 'is_vendor', )
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            password=self.validated_data['password'],
            is_vendor=self.validated_data['is_vendor'],
        )
        user.save()
        Token.objects.create(user=user)
        return user

class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ( 'id', 'user', 'first_name', 'last_name', )

class VendorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile
        fields = ( 'id', 'user', 'business_name', )

