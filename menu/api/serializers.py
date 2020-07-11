from rest_framework import serializers
from ..models import Menu


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ( 'id', 'name', 'description', 'price', 'quantity', 'scheduled_days', 'vendor', )
    '''
    def create(self, validated_data):
        if self.request.user.is_vendor:
            menu = Menu.objects.create(
                name = validated_data['name'],
                description = request.data['description'],
                quantity = request.data['quantity'],
                price = request.data['price'],
                vendor = request.user,
            )
            scheduled_days = (request.data['scheduled_days']).strip().split(' ')
            for scheduled_day in scheduled_days:
                menu.scheduled_days.add(Day.objects.get(name=scheduled_day))
            data = MenuSerializer(menu).data
            return Response({ 'detail': 'getting there' })
        raise PermissionError
    '''