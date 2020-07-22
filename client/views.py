import requests
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions
from rest_framework.authtoken.views import Token
from rest_framework.decorators import api_view, permission_classes

from user.user_model.user import User
from menu.models import Menu
from .forms import LoginForm


@api_view(['GET'])
@permission_classes([ permissions.AllowAny, ])
def index(request):
    if request.user.is_authenticated:
        return redirect('/users/profile/')
    context = { 'detail' : 'Welcome on board' }
    return render(request, 'index.html', context)

@permission_classes([permissions.AllowAny, ])
def createLogin(request):
    if request.user.is_authenticated:
        return redirect('/users/profile/')
    elif request.method == 'GET':
        context = { 'detail' : 'New Login Creation'}
        return render(request, 'login_create_form.html', context)
    elif request.method == 'POST':
        url = 'http://localhost:8000/api/accounts/create/'
        response = requests.post(url, data=request.POST)
        if response.status_code == 201:
            context = { 'detail' : 'Login created! Login to your profile. ' }
            return render(request, 'index.html', context)
        return render(request, '400.html', {'error':f'{response.content}'})

@api_view(['POST'])
@permission_classes( [permissions.AllowAny,] )
def loginView(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/users/profile/')
    context = { 'error': 'Login details not valid.'}
    return render(request, '400.html', context)

@api_view(['GET'])
@permission_classes( [permissions.AllowAny,] )
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        context = { 'detail' : 'Successful logout.' }
        return render(request, 'index.html', context)
    return redirect('/')
    
def profileView(request):
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = 'http://localhost:8000/api/accounts/profile/'
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            context = { 'detail': 'No profile' }
        elif response.status_code == 200:
            context = response.json()
            context['user'] = user
        return render(request, 'profile.html', context)
    elif request.method == 'POST':
        if user.is_vendor:
            data = { 'business_name': request.POST.get('business_name'), }
            response = requests.post(url, data=data, headers=headers)
        else:
            data = { 'first_name': request.POST.get('first_name'), 'last_name': request.POST.get('last_name'), }
            response = requests.post(url, data=data, headers=headers)
        if response.status_code == 201:
            return redirect('/users/profile/')
        return render(request, '400.html', { 'error': response.json() })

def notificationsView(request):
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = 'http://localhost:8000/api/notifications/'
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        notifications = response.json()
        context = { 'user': user, 'notifications': notifications }
        return render(request, 'notifications.html', context)
    elif request.method == 'POST':
        receiver = User.objects.get(email=request.POST.get('receiver'))
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        data = { 'sender': user.id, 'receiver': receiver.id, 'subject': subject, 'body': body }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 201:
            return redirect('/notifications/')
        return render(request, '400.html', { 'error': response.json() })

@api_view(['GET'])
def notificationDetailView(request, pk):
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = f'http://localhost:8000/api/notifications/{pk}/'
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return render(request, '404.html', {})
    elif response.status_code == 200:
        sender = response.json()['sender']
        sender_email = User.objects.get(pk=sender).email
        context = response.json()
        context['user'] = user
        context['sender_email'] = sender_email
        return render(request, 'notification-detail.html', context)

@api_view(['GET', 'POST'])
def menusView(request):
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = 'http://localhost:8000/api/menus/'
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        menus = response.json()
        context = { 'user': user, 'menus': menus }
        return render(request, 'menus.html', context)
    elif request.method == 'POST':
        data = { 
            'name': request.POST.get('name'), 'description': request.POST.get('description'),
            'quantity': request.POST.get('quantity'), 'price': request.POST.get('price'),
            'scheduled_days': request.POST.getlist('scheduled_days'), 'vendor': user.id 
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 201:
            return redirect('/menus/')
        return render(request, '400.html', { 'error': response.json() })

@api_view(['GET', 'POST'])
def menuDetailView(request, pk):
    days_order = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    days = []
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = f'http://localhost:8000/api/menus/{pk}/'
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        context = response.json()
        context['user'] = user
        for index in context['scheduled_days']:
            days.append(days_order[index])
        context['days'] = days
        return render(request, 'menu-detail.html', context)
    elif request.method == 'POST':
        response = requests.put(url, data=request.POST, headers=headers)
        if response.status_code == 201:
            return redirect('/menus/')
        return render(request, '400.html', {'error': response.json()})

@api_view([ 'GET', 'POST' ])
def ordersView(request):
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = 'http://localhost:8000/api/orders/'
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        orders = response.json()
        context = { 'user': user, 'orders': orders }
        return render(request, 'orders.html', context)
    elif request.method == 'POST':
        vendor = User.objects.get(email=request.POST.get('vendor'))
        due_date = request.POST.get('due_day')
        data = { 'customer': user.id, 'vendor': vendor.id, 'due_date': due_date }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 201:
            return redirect('/orders/')
        return render(request, '400.html', {'error': response.json()})

@api_view(['GET', 'POST'])
def orderDetailView(request, pk):
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = f'http://localhost:8000/api/orders/{pk}/'
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        customer = User.objects.get(pk=response.json()['customer'])
        vendor = User.objects.get(pk=response.json()['vendor'])
        context = response.json()
        context['menus'] = Menu.objects.filter(vendor=vendor)
        context['user'] = user
        context['order_customer'] = customer.email
        context['order_vendor'] = vendor.email
        context['order_items'] = requests.get(url+'items/', headers=headers).json()
        print(context)
        return render(request, 'order-detail.html', context)
    elif request.method == 'POST':
        print(request.POST)
        data = { 'order':pk, 'item':request.POST.get('item'), 'quantity':request.POST.get('quantity') }
        response = requests.post(url+'items/', data=data, headers=headers)
        print(response.json())
        if response.status_code == 201:
            return redirect(f'/orders/{pk}/')
        return render(request, '400.html', {'detail': response.json()['detail']})

@api_view(['GET', 'POST'])
def orderItemDetailView(request, pk, item_id):
    user = request.user
    token = Token.objects.get(user=user)
    headers = { 
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    url = f'http://localhost:8000/api/orders/{pk}/items/{item_id}/'
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        context = response.json()
        context['menuitem'] = Menu.objects.get(pk=response.json()['item']).name
        print(context)
        return render(request, 'orderitem-detail.html', context)
    elif request.method == 'POST':
        response = requests.delete(url, headers=headers)
        print(response.json())
        if response.status_code == 200:
            return redirect(f'/orders/{pk}/')
        return render(request, '400.html', {'detail': response.json()['detail']})
