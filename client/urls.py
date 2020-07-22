from django.urls import path
from django.views.generic import RedirectView
from .views import *


app_name = 'client'

urlpatterns = [
    path('', index, name='index_page'),
    path('api/', RedirectView.as_view(url='/')),
    path('create-login/', createLogin, name='create_login'),
    path('auth-login/', loginView, name='login_view'),
    path('auth-logout/', logoutView, name='logout_view'),
    path('users/profile/', profileView, name='profile_view'),
    path('notifications/', notificationsView, name='notifications_list'),
    path('notifications/<slug:pk>/', notificationDetailView, name='notifications_detail'),
    path('orders/', ordersView, name='orders_list'),
    path('orders/<slug:pk>/', orderDetailView, name='orders_detail'),
    path('orders/<slug:pk>/items/<slug:item_id>/', orderItemDetailView, name='orderitems_detail'),
    #path('orders/<slug:pk>/items/delete/<slug:item_id>/', orderItemDelete, name='orderitems_delete'),
    path('menus/', menusView, name='menus_list'),
    path('menus/<slug:pk>/', menuDetailView, name='menus_detail'),
]