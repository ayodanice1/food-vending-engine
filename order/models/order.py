import uuid

from django.db import models

from user.user_model.user import User


ORDER_STATUS_CHOICES=(
    ('OPEN', 'New Order'), 
    ('PLACED', 'Placed Order'), 
    ('RECEIVED', 'Received Order'),
    ('PROCESSING', 'Processing Order'),
    ('READY', 'Processed Order'), 
    ('DELIVERED', 'Delivered Order'), 
    ('CANCEL', 'Cancelling Order'), 
    ('CANCELLED', 'Cancelled Ordered'), 
)
PAYMENT_STATUS_CHOICES=(
    ('NYT', 'Not Yet Paid'), 
    ('PART', 'Partly Paid'), 
    ('FULL', 'Fully Paid'), 
)

class Order(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4 )
    customer = models.ForeignKey( 
        User, on_delete=models.CASCADE, limit_choices_to={'is_vendor':False},
        related_name='orders', blank=True, null=True 
    )
    vendor = models.ForeignKey( User, on_delete=models.CASCADE, limit_choices_to={'is_vendor':True} )
    total_order_cost = models.DecimalField( max_digits=10, decimal_places=2, default=0.0 )
    amount_paid = models.DecimalField( max_digits=10, decimal_places=2, default=0.0 ) 
    outstanding = models.DecimalField( max_digits=10, decimal_places=2, default=0.0 ) 
    time_created = models.DateTimeField( auto_now_add=True )
    order_status = models.CharField( max_length=10, choices= ORDER_STATUS_CHOICES, default='OPEN' )
    payment_status = models.CharField( max_length=4, choices= PAYMENT_STATUS_CHOICES, default='NYP' )
    
    class Meta:
        ordering = ['-time_created']
    
    def get_absolute_url(self):
        return reverse('order-detail-view', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.id} ({self.order_status})"
