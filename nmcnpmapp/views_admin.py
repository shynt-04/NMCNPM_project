from django.shortcuts import render
from .models import RoomUser
def account_management(request):
    accounts = RoomUser.objects.all()
    return render(request, 'app/account_management.html', {'accounts': accounts})