
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    url(r'^accounts/', include('allauth.urls')),
]
