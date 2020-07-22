from datetime import date

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models.aggregates import Sum

from ..models.order import Order
from ..models.orderitem import OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from ..orderpermissions import IsCustomer, IsConcerned, IsOwner

from user.user_model.user import User
from menu.models import Menu
from utils.orderutils import getDayFromDate, itemCanBeOrderedOnOrderDueDay


class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_vendor:
            queryset = Order.objects.filter(vendor=user)
        else:
            queryset = Order.objects.filter(customer=user)
        return queryset
    
    def post(self, request):
        if request.user.is_vendor:
            raise PermissionDenied
        data = { 
            'customer': request.user.id, 
            'vendor': request.data.get('vendor'), 
            'due_date': request.data.get('due_date'), 
        }
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = ( IsConcerned, )
    queryset = Order.objects.all()

    def put(self, request, pk):
        status_sequence = ('PLACED', 'RECEIVED', 'PROCESSING', 'READY', 'DELIVERED')
        order = get_object_or_404(Order, pk=pk)
        if order.vendor != request.user:
            raise PermissionDenied
        next_status = request.data.get('order_status')
        curr_status = order.order_status
        diff_in_sequence = status_sequence.index(next_status) - status_sequence.index(curr_status)
        if ( not next_status in status_sequence ) or diff_in_sequence != 1:
            return Response({'detail': 'Action failed.'}, status=status.HTTP_400_BAD_REQUEST)
        order.order_status = next_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.customer != request.user:
            raise PermissionDenied
        if order.order_status in ('OPEN', 'PLACED'):
            order.delete()
            return Response({'detail': 'Action successful'})
        elif order.order_status in ('PROCESSING', 'READY', 'RECEIVED'):
            order.outstanding = float(order.total_order_cost) * 0.4
            order.order_status = 'CANCEL'
            order.save()
            return Response(OrderSerializer(order).data)
        return Response({'detail': 'Action failed'}, status=status.HTTP_400_BAD_REQUEST)

class OrderItems(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        if self.request.user == order.vendor or self.request.user == order.customer:
            queryset = OrderItem.objects.filter(order_id=self.kwargs['pk'])
            return queryset
        else:
            raise PermissionDenied

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        item = get_object_or_404(Menu, pk=request.data.get('item'))
        if request.user != order.customer or item.vendor != order.vendor or order.order_status != 'OPEN':
            raise PermissionDenied
        order_due_day = getDayFromDate( order.due_date )
        if itemCanBeOrderedOnOrderDueDay( item, order_due_day ):
            data = { 'order': order.id, 'item': request.data.get('item'), 'quantity': request.data.get('quantity') }
            serializer = OrderItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Item not  scheduled for the due date.'}, status=status.HTTP_409_CONFLICT)
        
class OrderCheckout(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = ( IsOwner, )
    queryset = Order.objects.all()
    
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        outstanding = float(order.outstanding)
        try:
            amount_paid = float(request.data.get('amount_paid'))
        except ValueError:
            return Response({'detail': 'Action failed.'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        if order.order_status == 'OPEN':
            if amount_paid < outstanding:
                return Response({'detail': 'Action failed.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            order.order_status = 'PLACED'
        elif order.order_status == 'CANCEL':
            if amount_paid < outstanding:
                return Response({'detail': 'Action failed.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            order.order_status = 'CANCELLED'
        else:
            return Response({'detail': 'Action failed.'}, status=status.HTTP_409_CONFLICT)
        order.outstanding = outstanding - amount_paid
        order.amount_paid = amount_paid
        order.payment_status = 'PAID'
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
            
@api_view(['GET', 'DELETE'])
@permission_classes([ IsConcerned,] )
def orderItemDetail(request, pk, item_id):
    order = get_object_or_404(Order, pk=pk)
    orderitem = get_object_or_404(OrderItem, pk=item_id)
    if not order == orderitem.order:
        return Response({ 'detail': 'Order and item are not related.'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return Response(OrderItemSerializer(orderitem).data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        if order.order_status in ('OPEN', 'PLACED'):
            order.total_order_cost = float(order.total_order_cost) - float(orderitem.order_cost)
            order.outstanding = order.total_order_cost
            order.save()
            orderitem.delete()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        return Response({ 'detail': 'Cannot remove item.' }, status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
def salesReportView(request, date_string):
    user = request.user
    data = {}
    if not user.is_vendor:
        raise PermissionDenied
    vendor = User.objects.get(pk=user.id)
    orders = Order.objects.filter(vendor=vendor, date_created=date_string)
    if not orders:
        return Response({'detail': 'No orders found.'}, status=status.HTTP_204_NO_CONTENT)
    data['message'] = f'Sales Record for today, {date_string}'
    data['number_of_orders'] = orders.count()
    data['detail'] = [ 
        orders.aggregate(Sum('total_order_cost')), 
        orders.aggregate(Sum('amount_paid')), 
        orders.aggregate(Sum('outstanding')),
    ]
    return Response(data)
    
