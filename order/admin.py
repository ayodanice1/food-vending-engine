from django.contrib import admin

from .models.order import Order
from .models.orderitem import OrderItem


# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
