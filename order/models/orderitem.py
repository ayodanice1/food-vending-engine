import uuid

from django.db import models

from menu.models import Menu
from .order import Order


class OrderItem(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4 )
    order = models.ForeignKey( Order, on_delete=models.CASCADE, blank=True, null=True )
    item = models.ForeignKey( Menu, on_delete=models.CASCADE, blank=True, null=True )
    quantity = models.PositiveIntegerField( default=1 )
    order_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"{self.order} ({self.id})"
    
    def _set_order_cost(self):
        return float(self.item.price) * int(self.quantity)
    
    def save(self, *args, **kwargs):
        self.order_cost = self._set_order_cost()
        self.order.total_order_cost = float(self.order.total_order_cost) + self._set_order_cost()
        self.order.save()
        super().save(*args, **kwargs)

