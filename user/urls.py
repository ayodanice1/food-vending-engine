from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from .api import apiviews


urlpatterns = [
    path('users/', apiviews.UserList.as_view()),
    path('vendors/', apiviews.VendorList.as_view()),
    path('vendors/<str:pk>/', apiviews.vendorDetail),
    path('customers/', apiviews.CustomerList.as_view()),
    path('customers/<str:pk>/', apiviews.customerDetail),
    path('auth/register/', apiviews.UserCreate.as_view()),
    path('auth/profile/', apiviews.Profile.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
