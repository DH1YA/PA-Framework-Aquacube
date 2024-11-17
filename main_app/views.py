from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.
def cust_home(request): 
  return render(request, 'dashboard_customer/homepage.html')

def cust_agentform(request): 
  return render(request, 'dashboard_customer/agent.html')

def cust_productlist(request): 
  return render(request, 'dashboard_customer/product.html')

#================== agent =======================
def agent_productlist(request): 
  return render(request, 'dashboard_agent/product.html')

def agent_home(request): 
  return render(request, 'dashboard_agent/homepage.html')


#================= registration ===============
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect user berdasarkan grup atau role
            if user.groups.filter(name='ADMIN'):
                return redirect('/admin/')  # arahkan ke admin paner
            elif user.groups.filter(name='AGENT'):
                return redirect('agent_home')  # dashboard agent
            else:
                return redirect('cust_home')  # dashboard cutomer
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cust_home')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

