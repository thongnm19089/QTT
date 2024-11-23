# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
# from django.urls import reverse
from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict

from django.shortcuts import render, get_object_or_404
from .models import DonVi, Kho ,PhieuNhap ,PhieuXuat

from django.shortcuts import render, get_object_or_404, redirect
from .models import DonVi, Kho, QuanTuTrang, KhoQuanTrang
from django.contrib import messages


def kho_view(request, don_vi_id):
    # Lấy đơn vị và kho liên kết
    don_vi = get_object_or_404(DonVi, id=don_vi_id)
    kho = don_vi.kho  # Liên kết OneToOne giữa DonVi và Kho

    if request.method == 'POST':
        try:
            # Xử lý tạo loại quân tư trang mới
            if 'create_qtt' in request.POST:
                ten_qtt = request.POST.get('ten_qtt')
                loai_qtt = request.POST.get('loai_qtt')
                kich_co = request.POST.get('kich_co', '')
                mo_ta = request.POST.get('mo_ta', '')

                if not ten_qtt or not loai_qtt:
                    messages.error(request, "Vui lòng điền đầy đủ thông tin loại quân tư trang!")
                else:
                    QuanTuTrang.objects.create(
                        ten_qtt=ten_qtt,
                        loai_qtt=loai_qtt,
                        kich_co=kich_co,
                        mo_ta=mo_ta
                    )
                    messages.success(request, f"Đã tạo loại quân tư trang: {ten_qtt}.")

            # Xử lý nhập quân tư trang
            elif 'import_qtt' in request.POST:
                qtt_id = request.POST.get('qtt_id')
                so_luong = request.POST.get('so_luong')

                if not qtt_id or not so_luong or int(so_luong) <= 0:
                    messages.error(request, "Vui lòng chọn quân tư trang và nhập số lượng hợp lệ!")
                else:
                    quan_tu_trang = get_object_or_404(QuanTuTrang, id=qtt_id)
                    so_luong = int(so_luong)

                    # Nhập quân tư trang vào kho
                    kho_quan_trang, created = KhoQuanTrang.objects.get_or_create(
                        kho=kho,
                        quan_tu_trang=quan_tu_trang,
                        defaults={'so_luong': so_luong}
                    )
                    # if not created:
                    #     kho_quan_trang.so_luong += so_luong
                    #     kho_quan_trang.save()

                    # Lưu phiếu nhập
                    PhieuNhap.objects.create(kho=kho, quan_tu_trang=quan_tu_trang, so_luong_nhap=so_luong)
                    messages.success(request, f"Đã nhập {so_luong} {quan_tu_trang.ten_qtt} vào kho {kho.ten_kho}.")

            # Xử lý xuất quân tư trang
            elif 'export_qtt' in request.POST:
                qtt_ids = request.POST.getlist('qtt_id_export[]')  # Danh sách quân tư trang được chọn
                so_luong_exports = request.POST.getlist('so_luong_export[]')  # Danh sách số lượng tương ứng (chỉ nhận một số lượng)
                don_vi_nhan_id = request.POST.get('don_vi_nhan')  # Đơn vị nhận

                try:
                    # Lấy thông tin đơn vị nhận
                    don_vi_nhan = get_object_or_404(DonVi, id=don_vi_nhan_id)

                    # Nếu không có quân tư trang hoặc số lượng
                    if not qtt_ids or not so_luong_exports or len(so_luong_exports) != 1:
                        messages.error(request, "Vui lòng nhập đầy đủ thông tin để xuất!")
                        return redirect(request.path)

                    # Lấy số lượng chung từ form (áp dụng cho tất cả quân tư trang)
                    so_luong_export = int(so_luong_exports[0])
                    if so_luong_export <= 0:
                        messages.error(request, "Số lượng xuất phải lớn hơn 0!")
                        return redirect(request.path)

                    # Xử lý xuất cho từng quân tư trang
                    for qtt_id in qtt_ids:
                        try:
                            quan_tu_trang = get_object_or_404(QuanTuTrang, id=qtt_id)
                            kho_quan_trang = get_object_or_404(KhoQuanTrang, kho=kho, quan_tu_trang=quan_tu_trang)

                            if kho_quan_trang.so_luong >= so_luong_export:
                                # Giảm số lượng trong kho nguồn
                                # kho_quan_trang.so_luong -= so_luong_export
                                # kho_quan_trang.save()

                                # Thêm vào kho của đơn vị nhận
                                don_vi_kho = don_vi_nhan.kho
                                don_vi_kho_qtt, created = KhoQuanTrang.objects.get_or_create(
                                    kho=don_vi_kho,
                                    quan_tu_trang=quan_tu_trang,
                                    defaults={'so_luong': so_luong_export}
                                )
                                # if not created:
                                #     don_vi_kho_qtt.so_luong += so_luong_export
                                #     don_vi_kho_qtt.save()

                                # Lưu phiếu xuất
                                PhieuXuat.objects.create(
                                    kho=kho,
                                    quan_tu_trang=quan_tu_trang,
                                    so_luong_xuat=so_luong_export,
                                    don_vi_nhan=don_vi_nhan
                                )

                                messages.success(
                                    request,
                                    f"Đã xuất {so_luong_export} {quan_tu_trang.ten_qtt} đến {don_vi_nhan.ten_don_vi}."
                                )
                            else:
                                messages.error(
                                    request,
                                    f"Số lượng trong kho không đủ để xuất {quan_tu_trang.ten_qtt}!"
                                )
                        except (QuanTuTrang.DoesNotExist, KhoQuanTrang.DoesNotExist):
                            messages.error(request, f"Quân tư trang {qtt_id} không tồn tại trong kho!")

                except Exception as e:
                    messages.error(request, "Đã xảy ra lỗi trong quá trình xuất quân tư trang!")
                    print(f"Error: {e}")



        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi: {str(e)}")

    # Lấy danh sách quân tư trang trong kho
    quan_tu_trang_list = kho.khoquantrang_set.all()

    quan_tu_trang_list1 = QuanTuTrang.objects.all()

    don_vi_list = DonVi.objects.exclude(id=don_vi.id)

    grouped_don_vi = defaultdict(list)
    for dv in DonVi.objects.all():
        grouped_don_vi[dv.get_cap_do_display()].append(dv)
    grouped_don_vi = dict(grouped_don_vi)  # Chuyển defaultdict thành dict để tương thích với template

    return render(request, 'appstatic/kho_tong.html', {
        'don_vi': don_vi,
        'kho': kho,
        'quan_tu_trang_list': quan_tu_trang_list,
        'quan_tu_trang_list1': quan_tu_trang_list1,
        'don_vi_list': don_vi_list,
        'grouped_don_vi': grouped_don_vi
    })



def trung_doan_view(request):
    # Lấy danh sách đơn vị cấp Trung đoàn
    don_vi_trung_doan_list = DonVi.objects.filter(cap_do='trung_doan')
   
    if not don_vi_trung_doan_list.exists():
        messages.error(request, "Không tìm thấy đơn vị Trung đoàn nào.")
        return redirect('trang-chu')

    # Nếu chỉ lấy bản ghi đầu tiên
    don_vi_trung_doan = don_vi_trung_doan_list.first()
    kho_trung_doan = don_vi_trung_doan.kho
   
    # Logic POST (xuất quân tư trang) không thay đổi
    if request.method == 'POST' and 'export_qtt' in request.POST:
        qtt_id_export = request.POST.get('qtt_id_export')
        so_luong_export = request.POST.get('so_luong_export')
        don_vi_nhan_id = request.POST.get('don_vi_nhan')

        try:
            quan_tu_trang = QuanTuTrang.objects.get(id=qtt_id_export)
            don_vi_nhan = DonVi.objects.get(id=don_vi_nhan_id)
            so_luong_export = int(so_luong_export)

            kho_quan_trang = KhoQuanTrang.objects.get(kho=kho_trung_doan, quan_tu_trang=quan_tu_trang)
            if kho_quan_trang.so_luong >= so_luong_export:
                kho_quan_trang.so_luong -= so_luong_export
                kho_quan_trang.save()

                phieu_xuat = PhieuXuat.objects.create(
                    kho=kho_trung_doan,
                    quan_tu_trang=quan_tu_trang,
                    so_luong_xuat=so_luong_export,
                    don_vi_nhan=don_vi_nhan
                )
                messages.success(request, f"Đã xuất {so_luong_export} {quan_tu_trang.ten_qtt} đến {don_vi_nhan.ten_don_vi}")
            else:
                messages.error(request, "Không đủ số lượng trong kho để xuất.")
        except (QuanTuTrang.DoesNotExist, DonVi.DoesNotExist, KhoQuanTrang.DoesNotExist, ValueError):
            messages.error(request, "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.")

    quan_tu_trang_list = kho_trung_doan.khoquantrang_set.all()
    don_vi_list = DonVi.objects.exclude(cap_do='trung_doan')

    return render(request, 'appstatic/trung_doan.html', {
        'don_vi_trung_doan': don_vi_trung_doan,
        'kho_trung_doan': kho_trung_doan,
        'quan_tu_trang_list': quan_tu_trang_list,
        'don_vi_list': don_vi_list,
    })



def phieu_xuat_list_view(request):
    phieu_xuat_list = PhieuXuat.objects.all().order_by('-ngay_xuat')
    don_vi_list12 = DonVi.objects.all()  # Loại trừ chính đơn vị hiện tại

    grouped_don_vi = defaultdict(list)

    for don_vi in don_vi_list12:  # Lặp qua danh sách đơn vị
        grouped_don_vi[don_vi.get_cap_do_display()].append(don_vi)

    # Chuyển đổi defaultdict thành dict
    grouped_don_vi = dict(grouped_don_vi)
    return render(request, 'appstatic/phieu_xuat.html', {
        'phieu_xuat_list': phieu_xuat_list,
         'grouped_don_vi': grouped_don_vi
    })
def nhap_view(request):
    don_vi_list12 = DonVi.objects.all()  # Loại trừ chính đơn vị hiện tại

    grouped_don_vi = defaultdict(list)

    for don_vi in don_vi_list12:  # Lặp qua danh sách đơn vị
        grouped_don_vi[don_vi.get_cap_do_display()].append(don_vi)

    # Chuyển đổi defaultdict thành dict
    grouped_don_vi = dict(grouped_don_vi)
        
    phieu_nhap_list = PhieuNhap.objects.all().order_by('-ngay_nhap')  
    kho_id = request.GET.get('kho_id') 
    if kho_id:
        try:
            kho = Kho.objects.get(id=kho_id)
            phieu_nhap_list = phieu_nhap_list.filter(kho=kho)
        except Kho.DoesNotExist:
            pass 
    return render(request, 'appstatic/phieu_nhap.html', {
        'phieu_nhap_list': phieu_nhap_list,
        'grouped_don_vi': grouped_don_vi

    })


def home(request):
    return render(request, 'appstatic/home.html')

def redirect_to_home(request):
    return redirect('home')  # Redirect to the URL named 'home'

def contact(request):
    return render(request, 'appstatic/contact.html')

def about(request):
    return render(request, 'appstatic/about.html')

def user_login(request): 
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Chuyển hướng đến trang chính
     return render(request, "appstatic/login.html") 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
           
            # if username == 'qlqt@tieudoan20' and password == 'd20_qlqt':
            if username == 'thongnm' and password == 'a':
                return redirect('D20') 
            else:
                return redirect('home')  
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'appstatic/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  

@login_required(login_url="login")
def D20_view(request):
    don_vi_list12 = DonVi.objects.all()  # Loại trừ chính đơn vị hiện tại

    grouped_don_vi = defaultdict(list)

    for don_vi in don_vi_list12:  # Lặp qua danh sách đơn vị
        grouped_don_vi[don_vi.get_cap_do_display()].append(don_vi)

    # Chuyển đổi defaultdict thành dict
    grouped_don_vi = dict(grouped_don_vi)
    return render(request, 'appstatic/D20_1.html' ,{
        
        'grouped_don_vi': grouped_don_vi
    } )  

