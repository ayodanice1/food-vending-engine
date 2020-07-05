import uuid

from django.db import models
from django.urls import reverse

from .user_model.user import User


# Create your models here.
class VendorProfile(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4 )
    user = models.OneToOneField( User, on_delete=models.CASCADE )
    business_name = models.CharField( max_length=150, blank=True, null=True ) 
    
    class Meta:
        ordering = ['business_name']
    
    def get_email(self):
        return self.user.email
    
    def get_phone_number(self):
        return self.user.phone_number
    
    def get_absolute_url(self):
        return reverse('VendorDetailView', args=[str(self.id)])
    
    def __str__(self):
        return self.business_name


class CustomerProfile(models.Model):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4 )
    user = models.OneToOneField( User, on_delete=models.CASCADE )
    first_name = models.CharField( max_length=150, blank=True, null=True )
    last_name = models.CharField( max_length=150, blank=True, null=True )
    
    class Meta:
        ordering = ['first_name']
    
    def get_full_name(self):
        return "self.first_name self.last_name".strip()
    
    def get_short_name(self):
        return self.first_name
    
    def get_email(self):
        return self.user.email
    
    def get_phone_number(self):
        return self.user.phone_number
    
    def get_absolute_url(self):
        return reverse('CustomerDetailView', args=[str(self.id)])
    
    def __str__(self):
        return self.first_name
    