from django.contrib import admin
from django.urls import path
from appQLQT import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'), 
    path('', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),  
    path('D20/', views.D20_view, name='D20'),  
    path('kho/<int:don_vi_id>/', views.kho_view, name='kho'),
    path('trung-doan/', views.trung_doan_view, name='trung-doan'),
    path('nhap/', views.nhap_view, name='nhap'),
    path('xuat/', views.phieu_xuat_list_view, name='xuat'),


]
