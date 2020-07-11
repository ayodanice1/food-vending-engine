from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from .api import apiviews


urlpatterns = [
    path('menus/', apiviews.MenuList.as_view(), name='menus_list'),
    path('menus/<str:pk>/', apiviews.MenuDetail.as_view(), name='menus_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
