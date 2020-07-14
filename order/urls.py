from django.urls import path
from .api import apiviews


urlpatterns = [
    path('orders/', apiviews.OrderList.as_view(), name='orders_list'),
    path('orders/<slug:pk>/', apiviews.OrderDetail.as_view(), name='orders_detail'),
    path('orders/<str:pk>/checkout/', apiviews.OrderCheckout.as_view(), name='orders_checkout'),
    path('orders/<slug:pk>/items/', apiviews.OrderItems.as_view(), name='orderitems_list'),
    path('orders/<slug:pk>/items/<str:item_id>/', apiviews.OrderItemDetail.as_view(), name='orderitems_detail'),
    path('sales/<slug:date_string>/', apiviews.salesReportView, name='sales_report'),
]