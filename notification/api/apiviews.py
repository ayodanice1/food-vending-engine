from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from user.user_model.user import User

from ..models import Notification
from .serializers import NotificationSerializer


class NotificationList(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        queryset = Notification.objects.filter(sender=self.request.user)
        if not queryset:
            queryset = Notification.objects.filter(receiver=self.request.user)
        return queryset

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
            raise PermissionDenied 
        return Response(data)

    def delete(self, request, pk):
        return Response({ 'detail': 'Still working on notification deletion.' })
