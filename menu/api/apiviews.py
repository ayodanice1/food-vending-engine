from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from ..models import Day, Menu
from .serializers import MenuSerializer


class MenuList(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    
    def get_queryset(self):
        if self.request.user.is_vendor:
            queryset = Menu.objects.filter(vendor=self.request.user)
        else:
            queryset = Menu.objects.all()
        return queryset
    
    def post(self, request):
        if request.user.id != int(request.data['vendor']):
            raise PermissionDenied
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuDetail(generics.RetrieveUpdateAPIView):
    serializer_class = MenuSerializer
    
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        if menu.vendor == request.user or not request.user.is_vendor:
            data = MenuSerializer(menu).data
            return Response(data)
        raise PermissionDenied

    def put(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        if menu.vendor != request.user:
            raise PermissionDenied
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
