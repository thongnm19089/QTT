

from django.contrib import admin
from django.urls import path, include
from appQLQT import views

urlpatterns = [
    path('admin/', admin.site.urls),


    path('',include('appQLQT.urls')),
]



