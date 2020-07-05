from rest_framework import authentication, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..user_model.user import User
from ..models import ( CustomerProfile, VendorProfile, )
from .serializers import ( UserSerializer, CustomerProfileSerializer, VendorProfileSerializer )


class UserCreate(generics.CreateAPIView):
    permission_classes = ( permissions.AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    #permission_classes = ( permissions.IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerList(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

class VendorList(generics.ListAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer

class Profile(APIView):
    
    def _getProfile(self, profile_model, user):
        try:
            profile = profile_model.objects.get(user=user)
        except profile_model.DoesNotExist:
            return
        else:
            return profile

    # View a profile
    def get(self, request):
        user = request.user
        data = dict()
        profile = self._getProfile(CustomerProfile, user)
        if not profile:
            profile = self._getProfile(VendorProfile, user)
            if not profile:
                data['detail'] = 'No profile found. Create one.'
                return Response(data)
            data = VendorProfileSerializer(profile).data
        else:
            data = CustomerProfileSerializer(profile).data
        return Response(data)
    
    # Create a profile
    def post(self, request):
        user = request.user
        if user.is_vendor:
            profile = VendorProfile.objects.create(
                user=User.objects.get(pk=request.user.id),
                business_name=request.data["business_name"])
            profile.save()
        else:
            profile = CustomerProfile.objects.create(
                user=User.objects.get(pk=request.user.id),
                first_name=request.data["first_name"],
                last_name=request.data["last_name"])
            profile.save()
        return self.get(request)
    
@api_view(['GET'])
def customerDetail(request, pk):
    customer = CustomerProfile.objects.get(pk=pk)
    data = {
        'detail' : {
            'customer_id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.user.email,
            'phone_number': customer.user.phone_number,
        }
    }
    return Response(data)

@api_view(['GET'])
def vendorDetail(request, pk):
    vendor = VendorProfile.objects.get(pk=pk)
    data = {
        'detail' : {
            'vendor_id': vendor.id,
            'business_name': vendor.business_name,
            'email': vendor.user.email,
            'phone_number': vendor.user.phone_number,
        }
    }
    return Response(data)