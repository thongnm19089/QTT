
from django.contrib import admin
from .models import (
    Kho, DonVi, QuanNhan, QuanTuTrang, KhoQuanTrang,
    DonViQuanTrang, PhieuNhap, PhieuXuat, PhieuNhan,
    PhieuCapPhat, PhieuXacNhan, Kho
)





@admin.register(Kho)
class KhoAdmin(admin.ModelAdmin):
    list_display = ['ten_kho', 'quan_li_kho']
    search_fields = ['ten_kho', 'quan_li_kho__username']

@admin.register(DonVi)
class DonViAdmin(admin.ModelAdmin):
    list_display = ('ten_don_vi', 'cap_do', 'quan_li', 'don_vi_cha')
    search_fields = ('ten_don_vi', 'cap_do')
    list_filter = ('cap_do',)

@admin.register(QuanNhan)
class QuanNhanAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'don_vi', 'ngay_sinh', 'so_bien_nhan')
    search_fields = ('ho_ten', 'so_bien_nhan')
    list_filter = ('don_vi',)

@admin.register(QuanTuTrang)
class QuanTuTrangAdmin(admin.ModelAdmin):
    list_display = ( 'ten_qtt', 'loai_qtt', 'kich_co')
    search_fields = ('ten_qtt', 'loai_qtt')
    list_filter = ('loai_qtt',)

@admin.register(KhoQuanTrang)
class KhoQuanTrangAdmin(admin.ModelAdmin):
    list_display = ('kho', 'quan_tu_trang', 'so_luong')
    list_filter = ('kho', 'quan_tu_trang')
    search_fields = ('kho__ten_kho', 'quan_tu_trang__ten_qtt')

@admin.register(DonViQuanTrang)
class DonViQuanTrangAdmin(admin.ModelAdmin):
    list_display = ('don_vi', 'quan_tu_trang', 'so_luong')
    list_filter = ('don_vi', 'quan_tu_trang')
    search_fields = ('don_vi__ten_don_vi', 'quan_tu_trang__ten_qtt')

@admin.register(PhieuNhap)
class PhieuNhapAdmin(admin.ModelAdmin):
    list_display = ('code', 'kho', 'quan_tu_trang', 'so_luong_nhap', 'ngay_nhap')
    search_fields = ('code',)
    list_filter = ('ngay_nhap', 'kho', 'quan_tu_trang')

@admin.register(PhieuXuat)
class PhieuXuatAdmin(admin.ModelAdmin):
    list_display = ('code', 'kho', 'quan_tu_trang', 'so_luong_xuat', 'ngay_xuat', 'don_vi_nhan')
    search_fields = ('code',)
    list_filter = ('ngay_xuat', 'kho', 'quan_tu_trang', 'don_vi_nhan')

@admin.register(PhieuNhan)
class PhieuNhanAdmin(admin.ModelAdmin):
    list_display = ('phieu_xuat', 'don_vi_nhan', 'so_luong_nhan', 'ngay_nhan')
    list_filter = ('ngay_nhan', 'don_vi_nhan')

@admin.register(PhieuCapPhat)
class PhieuCapPhatAdmin(admin.ModelAdmin):
    list_display = ('don_vi_giao', 'don_vi_nhan', 'quan_tu_trang', 'so_luong_cap_phat', 'ngay_cap_phat', 'da_nhan')
    list_filter = ('ngay_cap_phat', 'don_vi_giao', 'don_vi_nhan', 'da_nhan')
    search_fields = ('don_vi_giao__ten_don_vi', 'don_vi_nhan__ten_don_vi', 'quan_tu_trang__ten_qtt')

@admin.register(PhieuXacNhan)
class PhieuXacNhanAdmin(admin.ModelAdmin):
    list_display = ('phieu_cap_phat', 'don_vi_nhan', 'da_xac_nhan')
    list_filter = ('da_xac_nhan', 'don_vi_nhan')
    search_fields = ('phieu_cap_phat__don_vi_giao__ten_don_vi', 'don_vi_nhan__ten_don_vi')
