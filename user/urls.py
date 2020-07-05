from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from .api import apiviews


urlpatterns = [
    path('users/', apiviews.UserList.as_view()),
    path('users/vendors/', apiviews.VendorList.as_view()),
    path('users/vendors/<str:pk>/', apiviews.vendorDetail),
    path('users/customers/', apiviews.CustomerList.as_view()),
    path('users/customers/<str:pk>/', apiviews.customerDetail),
    path('users/register/', apiviews.UserCreate.as_view()),
    path('users/profile/', apiviews.Profile.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
