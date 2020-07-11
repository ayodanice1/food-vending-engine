from rest_framework import serializers
from user.user_model.user import User

from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ( 'id', 'sender', 'receiver', 'subject', 'body', 'message_status' )
    
    def create(self, validated_data):
        receiver = User.objects.get(email=validated_data['receiver'])
        sender = User.objects.get(email=validated_data['sender'])
        if receiver == sender:
            raise PermissionError("Cannot send notification to self")
        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            subject=validated_data['subject'],
            body=validated_data['body'],
        )
        return notification

