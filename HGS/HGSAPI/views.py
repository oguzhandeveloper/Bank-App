from django.shortcuts import render, get_object_or_404


from .models import Tblhgs, Tblhgsurun

from django.contrib import messages

from random import randrange

from django.core import serializers
from django.http import JsonResponse
from django.http import HttpResponse



from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    return render(request, "index.html")


def registerhgs(request):
    tcNo = request.POST.get("tcNo")
    name = request.POST.get("name")
    lastname = request.POST.get("lastname")

    try:
        person = get_object_or_404(Tblhgs, tckimlikno=tcNo)
        return HttpResponse("Kullanıcı Zaten Kayıtlıdır.")
    except:
        pass

    number_ms = 000000000
    try:
        while True:
            number_ms = randrange(100000000, 999999999)
            hgs_ = get_object_or_404(Tblhgs, hgsno=number_ms)
    except:
        print("HGS Yok.")
        pass

    newPerson = Tblhgs(tckimlikno=tcNo, ad=name,
                       soyad=lastname, bakiye=0, hgsno=number_ms)
    newPerson.save()

    messages.success(
        request, "Register is Completed. If you want to add money your HGS product you have use OGUZ BANK for add money. Happy Day!")

    return render(request, "index.html")


def gethgsproduct(request):

    urunler = Tblhgsurun.objects.all()
    urunler_json = serializers.serialize('json', urunler)
    return HttpResponse(urunler_json, content_type='application/json')
    #return  HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def buyhgsproduct(request):
    id = request.POST.get("data")
    hgsurun = Tblhgsurun.objects.get(pk=id)
    hgsurun.delete()

    return HttpResponse("İşlem Tamamlandı.")

    


def addmoney(request):
    pass
