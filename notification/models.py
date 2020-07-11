import uuid

from django.db import models
from user.user_model.user import User


# Create your models here.
class Notification(models.Model):
    MESSAGE_STATUS_CHOICES = (
        ('NEW', 'New Notification'),
        ('READ', 'Notification Read'),
    )
    id = models.UUIDField( primary_key=True, default=uuid.uuid4 )
    subject = models.CharField(max_length=200)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sending_party')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    message_status = models.CharField(max_length=10, choices=MESSAGE_STATUS_CHOICES, default='NEW')
    
    class Meta:
        ordering = ('-time_created',)
    
    def __str__(self):
        return f"{self.subject} ({self.message_status})"
    
    def save(self, *args, **kwargs):
        if self.sender == self.receiver:
            return 'Cannot send notification to self'
        else:
            super().save(*args, **kwargs)
