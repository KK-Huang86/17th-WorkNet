from django.urls import path
from . import views

app_name = "notifications"

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
       path("", views.notifications_list, name="list"),
] + debug_toolbar_urls()
