from django.shortcuts import render

from .models import Notification

# Create your views here.


# 所有的通知，並按照時間的新舊順序排列
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.ueser).order_by(
        "-date_set"
    )
