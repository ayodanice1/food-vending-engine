from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import NotificationSerializer

from ..models import Notification
from .serializers import NotificationSerializer

from user.user_model.user import User



class NotificationList(APIView):
    
    def get(self, request):
        notifications = Notification.objects.filter(sender=request.user)
        if not notifications:
            notifications = Notification.objects.filter(receiver=request.user)
        data = NotificationSerializer(notifications, many=True).data
        return Response(data)
    
    def post(self, request):
        receiver = User.objects.get(email=request.data['receiver'])
        notification = Notification.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=request.data['subject'],
            body=request.data['body'],
        )
        return Response({ 'detail': 'notification sent'})


class NotificationDetail(APIView):

    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        if notification.receiver == request.user:
            notification.message_status='READ'
            notification.save()
            data = NotificationSerializer(notification).data
        elif notification.sender == request.user:
            data = NotificationSerializer(notification).data
        else:
            data['detail'] = 'permission denied' 
        return Response(data)

