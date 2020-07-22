from rest_framework import generics, permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes

from ..user_model.user import User
from ..models import ( CustomerProfile, VendorProfile, )
from .serializers import ( UserSerializer, CustomerProfileSerializer, VendorProfileSerializer )


class UserCreate(generics.CreateAPIView):
    permission_classes = ( permissions.AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    permission_classes = ( permissions.IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerList(generics.ListAPIView):
    permission_classes = ( permissions.IsAdminUser, )
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

class VendorList(generics.ListAPIView):
    permission_classes = ( permissions.IsAdminUser, )
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer

class Profile(APIView):
    renderer_classes = ( JSONRenderer, )
    
    def _getProfile(self, profile_model, user):
        try:
            profile = profile_model.objects.get(user=user)
        except profile_model.DoesNotExist:
            return
        return profile

    # View a profile
    def get(self, request):
        user = request.user
        data = dict()
        profile = self._getProfile(CustomerProfile, user)
        if not profile:
            profile = self._getProfile(VendorProfile, user)
            if not profile:
                data = { "detail": "Profile empty." }
                return Response( data, status=status.HTTP_204_NO_CONTENT )
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
                business_name=request.data["business_name"]
            )
            data = VendorProfileSerializer(profile).data
        else:
            profile = CustomerProfile.objects.create(
                user=User.objects.get(pk=request.user.id),
                first_name=request.data["first_name"],
                last_name=request.data["last_name"]
            )
            data = CustomerProfileSerializer(profile).data
        return Response(data, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@renderer_classes([JSONRenderer])
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
@renderer_classes([JSONRenderer])
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