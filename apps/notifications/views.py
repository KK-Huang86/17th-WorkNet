from django.shortcuts import render

from .models import Notification

# Create your views here.



def notifications_list(request):
    # 所有的通知，並按照時間的新舊順序排列
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-date_set"
    )
    #未讀訊息的總數
    unread_count=Notification.objects.filter(user=request.user,is_read=False).count()

    return render(request,"notifications.html",{notifications:notifications,unread_count:unread_count})