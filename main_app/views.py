from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

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
def signin(request): 
  return render(request, 'dashboard_customer/signin.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cust_home')  # arahkan ke home customer
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
