from django.urls import path, include

from .api import apiviews


urlpatterns = [
    path('notifications/', apiviews.NotificationList.as_view()),
    path('notifications/<slug:pk>/', apiviews.NotificationDetail.as_view()),
]