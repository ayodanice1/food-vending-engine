from rest_framework import ( generics, permissions, status )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from ..models import Day, Menu
from .serializers import MenuSerializer

from ..menupermissions import IsVendor


@api_view(['GET', 'POST'])
@permission_classes([IsVendor])
def createMenu(request):
    if request.method == 'GET':
        return Response({'detail': 'method GET not allowed'})
    menu = Menu.objects.create(
        name = request.data['name'],
        description = request.data['description'],
        quantity = request.data['quantity'],
        price = request.data['price'],
        vendor = request.user,
    )
    menu.save()
    scheduled_days = (request.data['scheduled_days']).strip().split(' ')
    for scheduled_day in scheduled_days:
        menu.scheduled_days.add(Day.objects.get(name=scheduled_day))
    data = MenuSerializer(menu).data
    return Response(data)


class MenuList(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuDetail(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class ModifyMenu(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( IsVendor, )
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

