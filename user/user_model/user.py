from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator

from .manager import UserManager


phone_regex = RegexValidator(
    regex=r'0\d{10}',
    message="Phone number must be a mobile phone number"
)

class User(AbstractBaseUser):
    email = models.EmailField( unique=True )
    phone_number = models.CharField( validators=[phone_regex], max_length=11 )
    date_joined = models.DateTimeField( auto_now_add=True )
    is_superuser = models.BooleanField( default=False )
    is_active = models.BooleanField( default=True )
    is_staff = models.BooleanField( default=False )
    is_vendor = models.BooleanField( default=False )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ['email']
    
    def get_absolute_url(self):
        return reverse('user.api.apiviews.UserDetail', args=[str(self.id)])
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
