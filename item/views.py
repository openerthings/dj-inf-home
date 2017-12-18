from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template.engine import _context_instance_undefined
from django.template import RequestContext
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from .forms import UserForm, RFIdForm, RFIdDetForm, ItemInForm, ItemOutForm
from .models import Album, Song
from .models import RFId, RFIdDet, Item, ItemIn, ItemOut
from datetime import datetime
from django.utils import formats

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def listRFId(request):
    rfids = RFId.objects.all()
    return render(request, 'item/rfid.html', {'rfids': rfids})


def item_in(request):
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        if request.method == 'GET':
            if request.GET.get("op") == 'ADD':              # Data 입력폼
                form = ItemInForm(request.POST or None)
                context = {
                    'form': form,
                }
                return render(request, 'item/item_in1.html', context)
        else:
            form = ItemInForm(request.POST or None)
            if form.is_valid():                              # Data 저장
                item_id = request.POST.get('Item')
                item = get_object_or_404(Item, pk=item_id)
                obj = form.save(commit=False)
                obj.Item = item
                obj.save()
        # Data 조회화면
        itemins = ItemIn.objects.order_by('-pk')
        return render(request, 'item/item_in_list.html', {'itemins': itemins})


def item_out(request):
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        if request.method == 'GET':
            if request.GET.get("op") == 'ADD':              # Data 입력폼
                form = ItemOutForm(request.POST or None)
                context = {
                    'form': form,
                }
                return render(request, 'item/item_out1.html', context)
        else:
            form = ItemOutForm(request.POST or None)
            if form.is_valid():                              # Data 저장
                item_id = request.POST.get('Item')
                item = get_object_or_404(Item, pk=item_id)
                obj = form.save(commit=False)
                obj.Item = item
                obj.save()
        # Data 조회화면
        itemouts = ItemOut.objects.order_by('-pk')
        return render(request, 'item/item_out_list.html', {'itemouts': itemouts})


def rfids_add(request):
    template_name = 'item/rfid_add1.html'
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        error = False
        today = formats.date_format(datetime.now(), "Y-m-d")
        if request.method == 'POST':
            mfr_firm = request.POST.get('mfr_firm')
            mfr_date = request.POST.get('mfr_date')
            rfids = request.POST.get('rfids').strip()
            rfid_list = rfids.split('\r\n')

            i = 0
            try:
                with transaction.atomic():
                    for rfid in rfid_list:
                        i = i + 1
                        print("id='" + rfid + "'")
                        RFId.objects.create(rf_id=rfid, mfr_date=mfr_date, mfr_firm=mfr_firm)
                msg = "총" + str(i) + "건 성공했습니다."
                return render(request, template_name, {'error': error, 'message': msg, 'mfr_date': today})
            except IntegrityError:
                error = True
                msg = "RFID : '" + rfid + "'중복 데이타 입니다. "
                return render_to_response(template_name,
                                          {"error": error, "message": msg, 'mfr_firm': mfr_firm, 'mfr_date': mfr_date,
                                           'rfids': rfids, },
                                          context_instance=RequestContext(request))
        msg = "RFID를 여러개 등록할 수 있는 입력폼입니다."
        return render(request, template_name, {'error': error, 'message': msg, 'mfr_date': today})


# RFID 납품(출고)
def rfids_out(request):
    template_name = 'item/rfid_out1.html'
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        error = False
        today = formats.date_format(datetime.now(), "Y-m-d")
        if request.method == 'POST':
            f_firm = request.POST.get('f_firm')
            f_date = request.POST.get('f_date')
            rfids = request.POST.get('rfids').strip()
            rfid_list = rfids.split('\r\n')

            i = 0
            try:
                with transaction.atomic():
                    for rfid in rfid_list:
                        i = i + 1
                        print("id='" + rfid + "'")
                        obj = RFId.objects.get(pk=rfid)
                        if obj.rf_id_state == 'OUT':
                            raise ValueError("RFID : '" + rfid + "'는 " + obj.rf_id_state +"상태로 출고대상이 아닙니다.")
                        obj.rf_id_state = 'OUT'
                        obj.out_firm = f_firm
                        obj.out_date = f_date
                        obj.save()

                        RFIdDet.objects.create(RFId=obj, out_date=f_date)
                    msg = "총" + str(i) + "건 성공했습니다."
                    return render(request, template_name, {'error': error, 'message': msg, 'f_date': today})
            except RFId.DoesNotExist:
                msg = "RFID : '" + rfid + "'가 존재하지 않습니다."
            except ValueError as e:
                msg = e.args
            error = True
            return render_to_response(template_name,
                                      {"error": error, "message": msg, 'f_firm': f_firm, 'f_date': f_date,
                                       'rfids': rfids, },
                                      context_instance=RequestContext(request))
        msg = "RFID를 여러개 등록할 수 있는 입력폼입니다."
        return render(request, template_name, {'error': error, 'message': msg, 'f_date': today})


# RFID 수리입고
def rfids_in(request):
    template_name = 'item/rfid_in1.html'
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        error = False
        today = formats.date_format(datetime.now(), "Y-m-d")
        if request.method == 'POST':
            f_msg = request.POST.get('f_msg')
            f_date = request.POST.get('f_date')
            rfids = request.POST.get('rfids').strip()
            rfid_list = rfids.split('\r\n')

            i = 0
            try:
                with transaction.atomic():
                    for rfid in rfid_list:
                        i = i + 1
                        print("id='" + rfid + "'")
                        obj = RFId.objects.get(pk=rfid)
                        if obj.rf_id_state != 'OUT':
                            raise ValueError("RFID : '" + rfid + "'는 " + obj.rf_id_state +"상태로 출고되지 않은 제품입니다.")
                        # if obj.rf_id_state == 'OUT'
                        obj.rf_id_state = 'IN'
                        obj.in_date = f_date
                        obj.save()

                        det = RFIdDet.objects.filter(RFId=obj).last()
                        det.in_date = f_date
                        det.message = f_msg
                        det.save()
                        # print("--------------det  : " + str(det.count()))
                    msg = "총" + str(i) + "건 성공했습니다."
                    return render(request, template_name, {'error': error, 'message': msg, 'f_date': today})
            except RFId.DoesNotExist:
                error = True
                msg = "RFID : '" + rfid + "'가 존재하지 않습니다."
            except ValueError as e:
                msg = e.args
            error = True
            return render_to_response(template_name,
                                      {"error": error, "message": msg, 'f_msg': f_msg, 'f_date': f_date,
                                      'rfids': rfids, },
                                      context_instance=RequestContext(request))
        msg = "RFID를 여러개 등록할 수 있는 입력폼입니다."
        return render(request, template_name, {'error': error, 'message': msg, 'f_date': today})


def create_rfid(request):
    # print("create_album 111")
    # if True:
    #     return HttpResponse("create Album.....You're looking at question %s." % "question_id")

    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        form = RFIdForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            rfid = form.save(commit=False)
            rfid.save()
            return render(request, 'item/detail.html', {'rfid': rfid})
        context = {
            "form": form,
        }
        return render(request, 'item/create_album.html', context)


def create_rfiddet(request, rfid_rf_id):
    form = RFIdDetForm(request.POST or None, request.FILES or None)
    rfid = get_object_or_404(RFId, pk=rfid_rf_id)
    if form.is_valid():
        rfiddet = form.save(commit=False)
        rfiddet.RFId = rfid
        # rfiddet.rf_id_state = "납품"
        rfiddet.save()
        return render(request, 'item/detail.html', {'rfid': rfid})
    context = {
        'rfid': rfid,
        'form': form,
    }
    return render(request, 'item/create_song.html', context)


def delete_rfid(request, rfid_rf_id):
    rfid = RFId.objects.get(pk=rfid_rf_id)
    rfid.delete()
    rfids = RFId.objects.all()
    return render(request, 'item/index.html', {'rfids': rfids})


def delete_rfiddet(request, rfid_rf_id, rfiddet_id):
    rfid = get_object_or_404(RFId, pk=rfid_rf_id)
    det = RFIdDet.objects.get(pk=rfiddet_id)
    det.delete()
    return render(request, 'item/detail.html', {'rfid': rfid})


def detail(request, rfid_rf_id):
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        user = request.user
        rfid = get_object_or_404(RFId, pk=rfid_rf_id)
        return render(request, 'item/detail.html', {'rfid': rfid, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        rfids = RFId.objects.all()
        query = request.GET.get("q")
        if query:
            rfids = rfids.filter(
                Q(rf_id__icontains=query)
            ).distinct()
            return render(request, 'item/index.html', {
                'rfids': rfids,
            })
        else:
            return render(request, 'item/index.html', {'rfids': rfids})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'item/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'item/index.html', {'albums': albums})
            else:
                return render(request, 'item/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'item/login.html', {'error_message': 'Invalid login'})
    return render(request, 'item/login.html')


def register(request):
    print("views.register 1")
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'item/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'item/register.html', context)


def rfiddets(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'item/login.html')
    else:
        rfiddets = RFIdDet.objects.all()
        return render(request, 'item/songs.html', {
            'rfiddets': rfiddets,
        })
