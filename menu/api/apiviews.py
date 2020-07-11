from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Day, Menu
from .serializers import MenuSerializer


class MenuList(APIView):
    
    def get(self, request):
        if request.user.is_vendor:
            menus = Menu.objects.filter(vendor=request.user)
        else:
            menus = Menu.objects.all()
        data = MenuSerializer(menus, many=True).data
        return Response(data)
    
    def post(self, request):
        if request.user.is_vendor:
            menu = Menu.objects.create(
                name = request.data['name'],
                description = request.data['description'],
                quantity = request.data['quantity'],
                price = request.data['price'],
                vendor = request.user,
            )
            scheduled_days = (request.data['scheduled_days']).strip().split(' ')
            for scheduled_day in scheduled_days:
                menu.scheduled_days.add(Day.objects.get(name=scheduled_day))
            data = MenuSerializer(menu).data
            return Response(data)
        return Response({ 'detail': 'You do not have the permission to perform this action' })

class MenuDetail(APIView):
    
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        if menu.vendor == request.user or not request.user.is_vendor:
            data = MenuSerializer(menu).data
            return Response(data)
        return Response({ 'detail': 'You do not have the permission to perform this action' })

    def put(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        if menu.vendor != request.user:
            return Response({ 'detail': 'You do not have the permission to perform this action' })
        for k, v in request.data.items():
            if k == 'name':
                menu.name = v
            elif k == 'description':
                menu.description = v
            elif k == 'quantity':
                menu.quantity = int(v)
            elif k == 'price':
                menu.price = float(v)
            elif k == 'scheduled_days':
                return Response({ 'detail': 'Working on updating scheduled days'})
            menu.save()
        return Response({ 'detail': 'Menu info updated successfully' })
    
