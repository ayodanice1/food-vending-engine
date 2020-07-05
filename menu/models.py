import uuid

from django.db import models

from .menu_models.day import Day
from user.user_model.user import User


class Menu(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4 )
    name = models.CharField( max_length=100 )
    description = models.CharField( max_length=250 )
    price = models.DecimalField( max_digits=6, decimal_places=2, default=0.00 )
    quantity = models.PositiveIntegerField( default=1 )
    vendor = models.ForeignKey( User, on_delete=models.CASCADE, limit_choices_to={'is_vendor':True} )
    time_created = models.DateTimeField( auto_now=True)
    scheduled_days = models.ManyToManyField( 
        Day, related_name='reoccurs', 
        help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.' 
    )
    
    class Meta:
        ordering = [ 'name' ]

    def get_absolute_url(self):
        return reverse('menu-detail-view', args=[str(self.id)])
        
    def __str__(self):
        return self.name
