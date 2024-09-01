from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def notifications_list(request):
    # 列出所有的通知，並按照時間的新舊順序排列
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    #未讀訊息的總數
    unread_count=Notification.objects.filter(user=request.user,is_read=False).count()

    return render(request,"notifications.html",{"notifications":notifications,"unread_count":unread_count})