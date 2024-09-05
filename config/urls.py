"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

from lib.utils.env import is_dev

urlpatterns = [
    path("companies/", include("apps.companies.urls")),
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("jobs/", include("apps.jobs.urls")),
    path("posts/", include("apps.posts.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("resumes/", include("apps.resumes.urls")),
]

if is_dev():
    urlpatterns += debug_toolbar_urls()
