from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class IsVendor(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return
        return request.user and request.user.is_vendor
