from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import FamilyMember, CustomUser, PaymentStatus, Payment, Article
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved:
                login(request, user)
                return redirect('homepage')
            else:
                return render(request, 'myapp/wait.html')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def homepage(request):
    articles = Article.objects.all()
    return render(request, 'myapp/homepage.html', {'articles': articles})

def about(request):
    return render(request, 'myapp/about.html')

def contact(request):
    return render(request, 'myapp/contact.html')

def notification(request):
    return render(request, 'myapp/notification.html')

@login_required
def personal(request):
    user = request.user
    family_members = FamilyMember.objects.filter(room_id=user.room_id)
    context = {
        'family_members': family_members
    }
    return render(request, 'myapp/personal.html', context)

@login_required
def changepassword(request):
    user = CustomUser.objects.get(username=request.user.username)
    context = {
        'room_id': user.room_id,
        'username': user.username,
        'registry_email': user.registry_email,
        'phone_number': user.phone_number
    }
    return render(request, 'myapp/changepassword.html', context)
@login_required
def password_change_done(request):
    return render(request, 'myapp/homepage.html')

@login_required
def service(request):
    user = CustomUser.objects.get(username=request.user.username)
    payments = PaymentStatus.objects.filter(room_id=user.room_id)
    payment_infos = Payment.objects.filter(statuses__in=payments)
    user_info_list = [
        {
            'khoan_thu': payment.payment,
            'phi': payment_info.amount,
            'da_dong': payment.status,
            'han_nop': payment_info.date
        }
        for payment, payment_info in zip(payments, payment_infos)
    ]
    return render(request, 'myapp/service.html', {'user_info_list': user_info_list})

@login_required
def wait(request):
    form = CustomAuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        if user.is_approved:
            login(request, user)
            return redirect('homepage')
    return redirect('homepage')

@login_required
def service_view(request):
    user = request.user
    family_group = Group.objects.get(name='Tên group của bạn') 
    is_member = family_group.user_set.filter(id=user.id).exists()
    return render(request, 'service.html', {'is_member': is_member})
