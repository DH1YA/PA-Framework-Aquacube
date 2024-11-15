from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def customer_home(request):
    return render(request, 'dashboard_customer/homepage.html')

def customer_product(request):
    return render(request, 'dashboard_customer/product.html')

def customer_agent(request):
    return render(request, 'dashboard_customer/agent.html')

def customer_signin(request):
    return render(request, 'dashboard_customer/signin.html')

def customer_signup(request):
    return render(request, 'dashboard_customer/signup.html')

def agent_home(request):
    return render(request, 'dashboard_agent/homepage.html')

def agent_product(request):
    return render(request, 'dashboard_agent/product.html')
