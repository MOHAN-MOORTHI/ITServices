
# Create your views here.
from django.shortcuts import render
from .models import Service, Subscription
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, login as auth_login
from .forms import RegisterForm, OTPForm
import random
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import Service, Subscription
from .forms import ServiceForm
import razorpay
from django.conf import settings

def home(request):
    services = Service.objects.filter(active=True)
    return render(request, 'services/home.html', {'services': services})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            request.session['user_id'] = user.id
            send_mail('Your OTP', f'Your OTP is {otp}', 'your-email@gmail.com', [user.email])
            return redirect('otp')
    else:
        form = RegisterForm()
    return render(request, 'services/register.html', {'form': form})

def otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if request.session['otp'] == form.cleaned_data['otp']:
                user = User.objects.get(id=request.session['user_id'])
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('home')
    else:
        form = OTPForm()
    return render(request, 'services/otp.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'services/login.html', {'form': form})





@login_required
def home(request):
    services = Service.objects.filter(active=True)
    return render(request, 'services/home.html', {'services': services})




def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})

def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'services/service_confirm_delete.html', {'service': service})




def subscribe(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        address = request.POST['address']
        amount = service.service_price + (service.service_price * service.service_tax / 100)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        payment = client.order.create({'amount': int(amount * 100), 'currency': 'INR', 'payment_capture': '1'})
        subscription = Subscription.objects.create(
            user=request.user,
            service=service,
            address=address,
            transaction_id=payment['id'],
            amount=amount,
            payment_status='PENDING'
        )
        return redirect('payment', payment['id'])
    return render(request, 'services/subscribe.html', {'service': service})

def payment(request, transaction_id):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
    payment = client.order.fetch(transaction_id)
    if payment['status'] == 'paid':
        subscription = Subscription.objects.get(transaction_id=transaction_id)
        subscription.payment_status = 'SUCCESS'
        subscription.save()
    return render(request, 'services/payment.html', {'payment': payment})

