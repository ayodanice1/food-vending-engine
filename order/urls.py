from django.urls import path
from .api import apiviews


urlpatterns = [
    path('orders/', apiviews.OrderList.as_view()),
    path('orders/<str:pk>/', apiviews.OrderDetail.as_view()),
    path('orders/<str:pk>/checkout/', apiviews.OrderCheckout.as_view()),
]