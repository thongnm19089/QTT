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
    user_profile = request.user.profile
    print(user_profile)
    if request.method == 'POST':
        try:
            # Xử lý tạo loại quân tư trang mới
            if 'create_qtt' in request.POST:
                pass

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
                               
                                kho_quan_trang.so_luong -= so_luong_export
                                kho_quan_trang.save()
                                
                                # Cập nhật kho đích
                                don_vi_kho = don_vi_nhan.kho
                                don_vi_kho_qtt, created = KhoQuanTrang.objects.get_or_create(
                                    kho=don_vi_kho,
                                    quan_tu_trang=quan_tu_trang,
                                    defaults={'so_luong': 0}  # Đặt mặc định là 0
                                )
                                don_vi_kho_qtt.so_luong += so_luong_export  # Luôn cập nhật số lượng
                                don_vi_kho_qtt.save()
                                PhieuXuat.objects.create(
                                    kho=kho,
                                    quan_tu_trang=quan_tu_trang,
                                    so_luong_xuat=so_luong_export,
                                    don_vi_nhan=don_vi_nhan
                                )
                                PhieuNhap.objects.create(
                                                        kho=don_vi_nhan.kho,  # Phiếu nhập sẽ được tạo cho kho của đơn vị nhận
                                                        quan_tu_trang=quan_tu_trang,
                                                        so_luong_nhap=so_luong_export
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

    don_vi_list = DonVi.objects.all()

    if user_profile.cap_do == 'kho':
        don_vi_list = don_vi_list.filter(cap_do='tieu_doan')
    elif user_profile.cap_do == 'tieu_doan':
        don_vi_list = don_vi_list.filter(cap_do='dai_doi')
    elif user_profile.cap_do == 'dai_doi':
        don_vi_list = don_vi_list.filter(cap_do='trung_doi')
    elif user_profile.cap_do == 'trung_doi':
        don_vi_list = don_vi_list.filter(cap_do='trung_doi')
    # elif user_profile.cap_do == 'tieu_doan':
    #     don_vi_list = don_vi_list.filter(cap_do='trung_doi')
    
    # don_vi_list = don_vi_list[:1]
    # don_vi_list = DonVi.objects.all().order_by('code')  # hoặc thêm filter nếu cần
    grouped_don_vi = defaultdict(list)
    for dv in DonVi.objects.all().order_by('code'):
        grouped_don_vi[dv.get_cap_do_display()].append(dv)
    grouped_don_vi = dict(grouped_don_vi)
  

    return render(request, 'appstatic/kho_tong.html', {
        'don_vi': don_vi,
        'kho': kho,
        'quan_tu_trang_list': quan_tu_trang_list,
        'quan_tu_trang_list1': quan_tu_trang_list1,
        'don_vi_list': don_vi_list,
        'grouped_don_vi': grouped_don_vi,
        'user_profile': user_profile,
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import KhoQuanTrang

def delete_quan_tu_trang(request, kho_id, quan_tu_trang_id):
    # Get the KhoQuanTrang object
    kho_quan_trang = get_object_or_404(KhoQuanTrang, kho_id=kho_id, quan_tu_trang_id=quan_tu_trang_id)

    # Get the related Kho object to fetch the don_vi_id
    kho = kho_quan_trang.kho
    don_vi_id = kho.don_vi.id  # Get the don_vi_id from the Kho object

    # Delete the KhoQuanTrang object
    kho_quan_trang.delete()

    # Add a success message
    messages.success(request, "Quân tư trang đã được xóa thành công.")

    # Redirect to the kho view using the correct don_vi_id
    return redirect('kho', don_vi_id=don_vi_id)


from collections import defaultdict
from django.shortcuts import render
from .models import PhieuXuat, DonVi, UserProfile

def phieu_xuat_list_view(request):
    # Get the logged-in user
    user = request.user

    # Get the 'UserProfile' associated with the logged-in user
    try:
        user_profile = user.profile  # Access the user profile (assuming a OneToOneField)
    except UserProfile.DoesNotExist:
        user_profile = None  # Handle the case where no profile exists for the user

    # Check if the user has a valid profile and DonVi
    if user_profile and user_profile.don_vi:
        don_vi = user_profile.don_vi

        phieu_xuat_list = PhieuXuat.objects.filter(kho__don_vi=don_vi).order_by('-ngay_xuat')

        # Group 'DonVi' by 'cap_do'
        don_vi_list = DonVi.objects.exclude(id=don_vi.id)  # Exclude the user's DonVi to avoid showing it
        grouped_don_vi = defaultdict(list)

        for don_vi_item in don_vi_list:
            grouped_don_vi[don_vi_item.get_cap_do_display()].append(don_vi_item)

        # Convert defaultdict to dict
        grouped_don_vi = dict(grouped_don_vi)

        # Render the filtered 'PhieuXuat' and grouped 'DonVi' to the template
        don_vi = user_profile.don_vi

        return render(request, 'appstatic/phieu_xuat.html', {
            'phieu_xuat_list': phieu_xuat_list,
            'grouped_don_vi': grouped_don_vi,
            'don_vi': don_vi,
        })
    else:
        # Handle the case where the user doesn't have a 'UserProfile' or 'DonVi'
        return render(request, 'error_template.html', {'error_message': "You do not manage any DonVi."})

def nhap_view(request):
    user_profile = request.user.profile
    don_vi = user_profile.don_vi
    kho_records = Kho.objects.filter(don_vi=don_vi)
    

    don_vi_list12 = DonVi.objects.all()  # Loại trừ chính đơn vị hiện tại

    grouped_don_vi = defaultdict(list)

    for don_vi in don_vi_list12:  # Lặp qua danh sách đơn vị
        grouped_don_vi[don_vi.get_cap_do_display()].append(don_vi)

    # Chuyển đổi defaultdict thành dict
    grouped_don_vi = dict(grouped_don_vi)
        
    # phieu_nhap_list = PhieuNhap.objects.all().order_by('-ngay_nhap')  
    phieu_nhap_list = PhieuNhap.objects.filter(kho__in=kho_records).order_by('-ngay_nhap')  

    kho_id = request.GET.get('kho_id') 
    if kho_id:
        try:
            kho = Kho.objects.get(id=kho_id)
            phieu_nhap_list = phieu_nhap_list.filter(kho=kho)
        except Kho.DoesNotExist:
            pass 

    don_vi = user_profile.don_vi

    return render(request, 'appstatic/phieu_nhap.html', {
        'phieu_nhap_list': phieu_nhap_list,
        'grouped_don_vi': grouped_don_vi,
        'don_vi': don_vi

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
    if request.user.is_authenticated:
        return redirect('D20')  # Trang chủ sau khi đăng nhập

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('D20')  # Chuyển hướng đến trang chính sau khi đăng nhập thành công
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'appstatic/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  



from .models import DonVi

def get_current_user_don_vi(user_profile):
    # Trả về đơn vị của người dùng hiện tại
    don_vi = user_profile.don_vi
    return {
        'id': don_vi.id,
        'ten_don_vi': don_vi.ten_don_vi
    }
@login_required(login_url="login")
def D20_view(request):
    # Lấy user_profile từ người dùng hiện tại
    user_profile = request.user.profile  # Đây là đối tượng UserProfile của người dùng

    # Lấy đơn vị của người dùng hiện tại
    current_user_don_vi = get_current_user_don_vi(user_profile)
    don_vi = user_profile.don_vi
    # Truyền dữ liệu vào template
    return render(request, 'appstatic/D20_1.html', {
        'current_user_don_vi': current_user_don_vi,
        'don_vi': don_vi
    })

from django.shortcuts import render
from django.contrib import messages
from .models import QuanTuTrang

def manage_qtt(request):
    if request.method == 'POST':
        if 'create_qtt' in request.POST:
            # Tạo mới quân tư trang
            ten_qtt = request.POST.get('ten_qtt')
            loai_qtt = request.POST.get('loai_qtt')
            kich_co = request.POST.get('kich_co', '')
            ma_qtt = request.POST.get('ma_qtt', '')

            if not ten_qtt or not loai_qtt:
                messages.error(request, "Vui lòng điền đầy đủ thông tin loại quân tư trang!")
            else:
                QuanTuTrang.objects.create(
                    ten_qtt=ten_qtt,
                    loai_qtt=loai_qtt,
                    kich_co=kich_co,
                    ma_qtt=ma_qtt
                )
                messages.success(request, f"Đã tạo loại quân tư trang: {ten_qtt}.")
        
        elif 'update_qtt' in request.POST:
            # Cập nhật quân tư trang
            id = request.POST.get('id')  # Thay đổi từ 'ma_qtt' sang 'id'
            ma_qtt = request.POST.get('ma_qtt')
            ten_qtt = request.POST.get('ten_qtt')
            loai_qtt = request.POST.get('loai_qtt')
            kich_co = request.POST.get('kich_co', '')

            qtt = get_object_or_404(QuanTuTrang, id=id)
            qtt.ten_qtt = ten_qtt
            qtt.loai_qtt = loai_qtt
            qtt.kich_co = kich_co
            qtt.save()
            messages.success(request, f"Đã cập nhật quân tư trang: {ten_qtt}.")

        
        elif 'delete_qtt' in request.POST:
            ma_qtt = request.POST.get('ma_qtt')
            qtt = get_object_or_404(QuanTuTrang, id=ma_qtt)  # Tìm kiếm theo 'ma_qtt'
            qtt.delete()
            messages.success(request, f"Đã xóa quân tư trang: {ma_qtt}.")
    
    qtt_list = QuanTuTrang.objects.all()
    user_profile = request.user.profile  # Đây là đối tượng UserProfile của người dùng

    don_vi = user_profile.don_vi
    return render(request, 'appstatic/manage_qtt.html', {
        'qtt_list': qtt_list,
        'don_vi': don_vi
        }
                  )