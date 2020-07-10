from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from ..models.order import Order
from ..models.orderitem import OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from ..orderpermissions import IsCustomer, IsConcerned

from user.user_model.user import User
from menu.models import Menu


class OrderList(APIView):
    
    def get(self, request):
        user = request.user
        if user.is_vendor:
            orders = Order.objects.filter(vendor=user)
        else:
            orders = Order.objects.filter(customer=user)
        data = OrderSerializer(orders, many=True).data
        return Response(data)
    
    def post(self, request):
        if request.user.is_vendor:
            data = { 'detail' : 'you do not have the permission to perform this action' }
        vendor = User.objects.get(email=request.data['vendor'])
        order = Order.objects.create( vendor=vendor, customer=request.user, )
        return Response({ 'detail': 'action successful' })
    
class OrderDetail(APIView):
    
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.customer == request.user or order.vendor == request.user:
            data = dict()
            orderitems = OrderItem.objects.filter(order=order)
            data['order'] = OrderSerializer(order).data
            data['items'] = OrderItemSerializer(orderitems, many=True).data
            return Response(data)
        return Response({ 'detail': 'You do not have the permission to perform this action' })
    
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.customer != request.user:
            return Response({ 'detail': 'You do not have the permission to perform this action' })
        if order.order_status != 'OPEN':
            return Response({ 'detail': 'action failed' })
        orderitem = OrderItem.objects.create(
            order=order,
            item=Menu.objects.get(pk=request.data['item']),
            quantity=request.data['quantity'],
        )
        return Response({ 'detail': 'action successful' })

    def put(self, request, pk):
        status_sequence = ('PLACED', 'RECEIVED', 'PROCESSING', 'READY', 'DELIVERED')
        order = get_object_or_404(Order, pk=pk)
        if order.vendor != request.user :
            return Response({ 'detail': 'You do not have the permission to perform this action' })
        new_status = request.data['new_status']
        if not new_status in status_sequence:
            # Not all status are available to vendors
            return Response({ 'detail': 'action failed... invalid input' })
        elif status_sequence.index(new_status) - status_sequence.index(order.order_status) != 1:
            # Order status must change in sequence
            return Response({ 'detail': 'action failed' })
        order.order_status = new_status
        order.save()
        return Response({ 'detail': 'action successful' })

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if object.customer != request.user:
            return Response({ 'detail': 'You do not have the permission to perform this action' })
        if order.order_status in ('OPEN', 'PLACED'):
            # Orders not yet received by vendors can be deleted
            order.delete()
            return Response({ 'detail': 'action successful'})
        elif order.order_status in ('PROCESSING', 'READY', 'RECEIVED'):
            order.outstanding = float(order.total_order_cost) * 0.4
            order.order_status = 'CANCEL'
            order.save()
            return Response({ 'detail': 'action successful' })
        return Response({ 'detail': 'action failed' })

class OrderCheckout(APIView):

    def get(self, request, pk):
        if request.user.is_vendor:
            return Response({ 'detail': 'you do not have the permission to perform this action' })
        order = get_object_or_404(Order, pk=pk)
        if not order.customer == request.user:
            return Response({ 'detail': 'You do not have the permission to perform this action' })
        if order.order_status == 'OPEN':
            if order.total_order_cost == 0:
                order.delete()
                return Response({ 'detail': 'order void' })
            order.order_status = 'PLACED'                
            order.outstanding = float(order.total_order_cost)
            order.save()
        data = OrderSerializer(order).data
        return Response(data)
    
    def post(self, request, pk):
        if request.user.is_vendor:
            return Response({ 'detail': 'You do not have the permission to perform this action' })
        order = get_object_or_404(Order, pk=pk)
        outstanding = float(order.outstanding)
        amount_paid = float(request.data['amount_paid'])
        if order.order_status == 'OPEN':
            return Response({ 'detail': 'action failed... generate invoice first' })
        elif order.order_status == 'CANCELLED' or amount_paid < 10.0:
            return Response({ 'detail': 'action failed' })
        elif order.order_status == 'CANCEL':
            if amount_paid < outstanding:
                return Response({ 'detail': 'action failed' })
            order.order_status = 'CANCELLED'
            order.payment_status = 'FULL'
        else:
            if amount_paid < outstanding:
                order.payment_status = 'PART'
            order.payment_status = 'FULL'
        order.outstanding = outstanding - amount_paid
        order.amount_paid = amount_paid
        order.save()
        return Response({ 'detail': 'action successful'})
            
class OrderItemDetail(APIView):
    def get(self, request, pk):
        pass

    def post(self, request, pk):
        pass

    def put(self, request, pk):
        pass
    
    def delete(self, request, pk):
        if request.user.is_vendor:
            return Response({ 'detail': 'You do not have the permission to perform this action' })
        order = get_object_or_404(Order, pk=pk)
        if order.order_status in ('OPEN', 'PLACED'):
            order.delete()
            return Response({ 'detail': 'action successful'})
        elif order.order_status in ('PROCESSING', 'READY', 'RECEIVED'):
            order.outstanding = float(order.total_order_cost) * 0.4
            order.order_status = 'CANCEL'
            order.save()
            return Response({ 'detail': 'action successful' })
        return Response({ 'detail': 'action failed' })

