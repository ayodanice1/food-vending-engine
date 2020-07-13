import uuid

from django.db import models
from django.utils import timezone

from user.user_model.user import User


ORDER_STATUS_CHOICES=(
    ('OPEN', 'New Order'), 
    ('PLACED', 'Placed Order'), 
    ('RECEIVED', 'Received Order'),
    ('PROCESSING', 'Processing Order'),
    ('READY', 'Ready Order'), 
    ('DELIVERED', 'Delivered Order'), 
    ('CANCEL', 'Cancelling Order'), 
    ('CANCELLED', 'Cancelled Ordered'), 
)
PAYMENT_STATUS_CHOICES=(
    ('NYT', 'Not Yet Paid'), 
    ('PAID', 'Fully Paid'), 
)

class Order(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4 )
    customer = models.ForeignKey( 
        User, on_delete=models.CASCADE, limit_choices_to={'is_vendor':False},
        related_name='orders', blank=True, null=True 
    )
    vendor = models.ForeignKey( User, on_delete=models.CASCADE, limit_choices_to={'is_vendor':True} )
    due_date = models.DateField( default=timezone.now() )
    total_order_cost = models.DecimalField( max_digits=10, decimal_places=2, default=0.0 )
    amount_paid = models.DecimalField( max_digits=10, decimal_places=2, default=0.0 ) 
    outstanding = models.DecimalField( max_digits=10, decimal_places=2, default=0.0 ) 
    date_created = models.DateField( auto_now_add=True )
    order_status = models.CharField( max_length=10, choices= ORDER_STATUS_CHOICES, default='OPEN' )
    payment_status = models.CharField( max_length=4, choices= PAYMENT_STATUS_CHOICES, default='NYP' )
    
    class Meta:
        ordering = ['-date_created']
    
    def get_absolute_url(self):
        return reverse('OrderDetail', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.id} ({self.order_status})"
