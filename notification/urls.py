from django.urls import path, include

from .api import apiviews


urlpatterns = [
    path('notifications/', apiviews.NotificationList.as_view()),
    path('notifications/<int:pk>/', apiviews.NotificationDetail.as_view()),
]