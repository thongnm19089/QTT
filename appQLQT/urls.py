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
    path('nhap/', views.nhap_view, name='nhap'),
    path('xuat/', views.phieu_xuat_list_view, name='xuat'),
    path('manage_qtt/', views.manage_qtt, name='manage_qtt'),
    path('kho/<int:kho_id>/quan-tu-trang/<int:quan_tu_trang_id>/delete/', views.delete_quan_tu_trang, name='delete_quan_tu_trang'),


    # path('manage_qtt/update/', views.update_qtt, name='update_qtt'),
    # path('manage_qtt/delete/', views.delete_qtt, name='delete_qtt'),
]
