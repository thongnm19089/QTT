



from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import random
import string
from django.conf import settings
from django.contrib.auth import get_user_model

# Model Kho
DON_VI_CHOICES = [
        ('kho', 'Kho'),
        ('tieu_doan', 'Tiểu đoàn'),
        ('dai_doi', 'Đại đội'),
        ('trung_doi', 'Trung đội'),
  
    ]
class Kho(models.Model):
    ten_kho = models.CharField(max_length=100)
    don_vi = models.OneToOneField('DonVi', on_delete=models.CASCADE, related_name='kho',null=True)  # Mỗi đơn vị có 1 kho
    quan_li_kho = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_kho')

    def save(self, *args, **kwargs):
        # Nếu chưa có người quản lý kho, sử dụng người quản lý đơn vị
        if not self.quan_li_kho:
            self.quan_li_kho = self.don_vi.quan_li
        super(Kho, self).save(*args, **kwargs)

    def __str__(self):
        if self.don_vi:
            return f"{self.ten_kho} ({self.don_vi.ten_don_vi})"
        return f"{self.ten_kho} (Chưa liên kết đơn vị)"
    

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    cap_do = models.CharField(max_length=20, choices=DON_VI_CHOICES,null=True, blank=True)
    def __str__(self):
        return f"UserProfile for {self.user.username} - {self.get_cap_do_display()}"
    
class DonVi(models.Model):
    ten_don_vi = models.CharField(max_length=100)
    cap_do = models.CharField(max_length=20, choices=DON_VI_CHOICES)
    quan_li = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    don_vi_cha = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_units')
    dashboard_template = models.CharField(max_length=50, default='dashboard.html')
    code = models.CharField(max_length=50 , blank=True , null=True)
    def save(self, *args, **kwargs):
        # Nếu đối tượng DonVi chưa có quản lí, tự động tạo user mới
        if not self.quan_li:
            username = self.ten_don_vi.lower().replace(' ', '_')
            # Tạo user với mật khẩu mặc định là '123'
            user = User.objects.create_user(username=username, password='123')
            self.quan_li = user
        
        # Gọi phương thức save gốc
        super(DonVi, self).save(*args, **kwargs)
        
        # Tạo kho cho đơn vị nếu chưa tồn tại
        if not hasattr(self, 'kho'):
            Kho.objects.create(
                ten_kho=f"Kho của {self.ten_don_vi}",
                don_vi=self,
                quan_li_kho=self.quan_li
            )

    def __str__(self):
        return f"{self.ten_don_vi} ({self.get_cap_do_display()})"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    don_vi = models.ForeignKey('DonVi', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profiles')
    cap_do = models.CharField(max_length=20, choices=DON_VI_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"UserProfile for {self.user.username} - {self.get_cap_do_display()} - Don Vi: {self.don_vi.ten_don_vi if self.don_vi else 'Chưa có đơn vị'}"

    
User = get_user_model()

class QuanNhan(models.Model):
    ho_ten = models.CharField(max_length=100)
    don_vi = models.ForeignKey(DonVi, on_delete=models.CASCADE)
    ngay_sinh = models.DateField()
    so_bien_nhan = models.CharField(max_length=50)

    def __str__(self):
        return self.ho_ten

class QuanTuTrang(models.Model):
    # ma_qtt = models.CharField(max_length=10, primary_key=True)
    ma_qtt = models.CharField(max_length=100,null=True , blank=True)
    ten_qtt = models.CharField(max_length=100)
    loai_qtt = models.CharField(max_length=50)
    kich_co = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.ten_qtt}"

class KhoQuanTrang(models.Model):
    kho = models.ForeignKey(Kho, on_delete=models.CASCADE)
    quan_tu_trang = models.ForeignKey(QuanTuTrang, on_delete=models.CASCADE)  # Sử dụng id mặc định
    so_luong = models.PositiveIntegerField()

    class Meta:
        unique_together = ('kho', 'quan_tu_trang')

    def __str__(self):
        return f"{self.quan_tu_trang} - Số lượng: {self.so_luong}"

class DonViQuanTrang(models.Model):
    don_vi = models.ForeignKey(DonVi, on_delete=models.CASCADE)
    quan_tu_trang = models.ForeignKey(QuanTuTrang, on_delete=models.CASCADE)  # Sử dụng id mặc định
    so_luong = models.PositiveIntegerField()

    class Meta:
        unique_together = ('don_vi', 'quan_tu_trang')

    def __str__(self):
        return f"{self.don_vi} - {self.quan_tu_trang}: {self.so_luong}"

def generate_random_code(length=10):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not PhieuNhap.objects.filter(code=code).exists() and not PhieuXuat.objects.filter(code=code).exists():
            return code

class PhieuNhap(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)
    kho = models.ForeignKey(Kho, on_delete=models.CASCADE)
    quan_tu_trang = models.ForeignKey(QuanTuTrang, on_delete=models.CASCADE)
    so_luong_nhap = models.PositiveIntegerField()
    ngay_nhap = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_code()  # Hàm tạo mã phiếu
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Phiếu nhập {self.code} - {self.kho.ten_kho}"


class PhieuXuat(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)
    kho = models.ForeignKey(Kho, on_delete=models.CASCADE)
    quan_tu_trang = models.ForeignKey(QuanTuTrang, on_delete=models.CASCADE)
    so_luong_xuat = models.PositiveIntegerField()
    ngay_xuat = models.DateTimeField(auto_now_add=True)
    don_vi_nhan = models.ForeignKey(DonVi, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_code()
        try:
            # Kiểm tra QTT trong kho xuất
            kho_quan_trang = KhoQuanTrang.objects.get(kho=self.kho, quan_tu_trang=self.quan_tu_trang)
            if kho_quan_trang.so_luong >= self.so_luong_xuat:
                # Giảm số lượng từ kho xuất
                kho_quan_trang.so_luong -= self.so_luong_xuat
                kho_quan_trang.save()

                # Lấy kho của đơn vị nhận (trung đoàn)
                kho_nhan = self.don_vi_nhan.kho
                if kho_nhan:
                    # Tăng số lượng vào kho nhận
                    kho_nhan_quan_trang, created = KhoQuanTrang.objects.get_or_create(
                        kho=kho_nhan,
                        quan_tu_trang=self.quan_tu_trang,
                        defaults={'so_luong': self.so_luong_xuat}
                    )
                    if not created:
                        kho_nhan_quan_trang.so_luong += self.so_luong_xuat
                        kho_nhan_quan_trang.save()
                else:
                    raise ValueError("Kho của đơn vị nhận không tồn tại.")

            else:
                raise ValueError("Không đủ số lượng trong kho để xuất.")
        except KhoQuanTrang.DoesNotExist:
            raise ValueError("Quân tư trang không có trong kho.")
        super().save(*args, **kwargs)


class PhieuNhan(models.Model):
    don_vi_giao = models.ForeignKey(DonVi, on_delete=models.CASCADE, related_name='phieunhan_giao', null=True)
    phieu_xuat = models.ForeignKey(PhieuXuat, on_delete=models.CASCADE)
    don_vi_nhan = models.ForeignKey(DonVi, on_delete=models.CASCADE, related_name='phieunhan_nhan')
    so_luong_nhan = models.PositiveIntegerField()
    ngay_nhan = models.DateTimeField(auto_now_add=True)

class PhieuCapPhat(models.Model):
    don_vi_giao = models.ForeignKey(DonVi, related_name='don_vi_giao', on_delete=models.CASCADE)
    don_vi_nhan = models.ForeignKey(DonVi, related_name='don_vi_nhan', on_delete=models.CASCADE)
    quan_tu_trang = models.ForeignKey(QuanTuTrang, on_delete=models.CASCADE)
    so_luong_cap_phat = models.PositiveIntegerField()
    ngay_cap_phat = models.DateTimeField(auto_now_add=True)
    da_nhan = models.BooleanField(default=False)

class PhieuXacNhan(models.Model):
    phieu_cap_phat = models.ForeignKey(PhieuCapPhat, on_delete=models.CASCADE)
    don_vi_nhan = models.ForeignKey(DonVi, on_delete=models.CASCADE)
    da_xac_nhan = models.BooleanField(default=False)
