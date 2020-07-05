from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from .api import apiviews


urlpatterns = [
    path('menus/', apiviews.MenuList.as_view()),
    path('menus/<str:pk>/', apiviews.MenuDetail.as_view()),
    path('menus/<str:pk>/modify/', apiviews.ModifyMenu.as_view()),
    path('menus/add/', apiviews.createMenu),
]

urlpatterns = format_suffix_patterns(urlpatterns)
