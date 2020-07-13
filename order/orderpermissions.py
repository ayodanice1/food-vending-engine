from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return
        return request.user and not request.user.is_vendor

class IsConcerned(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return
        return request.user and request.user.is_active
    
    def has_object_permission(self, request, view, obj):
        if request.user == obj.vendor or request.user == obj.customer:
            return True
        return

class IsOwner(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return
        return request.user and request.user.is_active

    def has_object_permission(self, request, view, obj):
        if request.user == obj.customer:
            return True
        return
    
