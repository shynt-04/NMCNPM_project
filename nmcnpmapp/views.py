from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import FamilyMember, PaymentStatus, Payment, Article, RoomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the authenticated user
            user = form.get_user()
            if user:
                login(request, user)
                print(login(request, user))
                print(user.username)
                return redirect('homepage')
        else:
            # Check if the error was due to unapproved status
            if "awaiting approval" in str(form.errors):
                return render(request, 'app/wait.html')

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
    return render(request, 'app/homepage.html', {'articles': articles})

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def notification(request):
    return render(request, 'app/notification.html', {'articles': Article.objects.all()})

@login_required
def list_member(request):
    user = request.user
    try:
        # Fetch all family members for the logged-in user's room
        family_members = FamilyMember.objects.filter(room_id=user.room_id)
    except AttributeError:
        # If `user.roomuser` or `room_id` is not accessible, log this or handle it as needed
        family_members = []

    # Pass family_members directly to the template
    return render(request, 'app/member.html', {'family_members': family_members})


@login_required
def changepassword(request):
    user = RoomUser.objects.get(username=request.user.username)
    context = {
        'room_id': user.room_id,
        'username': user.username,
        'registry_email': user.registry_email,
        'phone_number': user.phone_number
    }
    return render(request, 'app/changepassword.html', context)

@login_required
def password_change_done(request):
    return render(request, 'app/homepage.html')

@login_required
def service(request):
    user = RoomUser.objects.get(username=request.user.username)
    payments = PaymentStatus.objects.filter(room_id=user.room_id)
    payment_infos = Payment.objects.filter(statuses__in=payments)
    payment_info_list = [
        {
            'khoan_thu': payment.payment,
            'phi': payment_info.amount,
            'da_dong': payment.status,
            'han_nop': payment_info.date
        }
        for payment, payment_info in zip(payments, payment_infos)
    ]
    return render(request, 'app/service.html', {'payment_info_list': payment_info_list})

@login_required
def add_member(request):
    if request.method == 'POST':
        # Fetch the RoomUser instance associated with the current user
        room_user = get_object_or_404(RoomUser, username=request.user.username)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Create the FamilyMember and assign the RoomUser instance
        FamilyMember.objects.create(
            room_id=room_user,
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email,
            phone_number=phone_number
        )
        return redirect('service')
    
    return render(request, 'app/add_member.html')

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
