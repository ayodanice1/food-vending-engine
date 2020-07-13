from rest_framework import serializers

from ..models.order import Order
from ..models.orderitem import OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ( 
            'id', 'customer', 'vendor', 'due_date', 'total_order_cost', 'amount_paid', 
            'date_created', 'outstanding', 'order_status', 'payment_status', )
    

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ( 'id', 'order', 'item', 'quantity', 'order_cost' )
    