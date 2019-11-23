import datetime
from .models import Tblhesapek, Havale, Tblhavaletip
from .models import Tblmusteri, Tblkisi, Tblhesap
from decimal import *
from random import randrange
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, render_to_response

from django.http import HttpResponse, HttpRequest


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt


from datetime import datetime

from django.db.models import Max
from django.utils import timezone



import json
import urllib



# Create your views here.

#Ana Sayfaya yönlendiren method
def index(request):
    return render(request, 'index.html')




#Navigation Bara yönlendiren sayfa/// TEST İÇİN YAZILIMIŞTIR
def navbar(reques):
    return render(reques, "navbar.html")




#Login Sayfasına yönlendiren method. /// LOGIN sayfasında aynı zamanda kayıt olunabilir.
def logpage(request):
    return render(request, 'login.html')




#Şifre Güncelleme sayfasına yönlendiren method
def updatepasswordpage(request):
    return render(request, 'updatepassword.html')





# Para ekleme sayfasına yönlendiren verilen hesap numarasını yönlendirildiği method
def addmoney(request):
    hesapno = request.POST.get("hesapno")
    return render(request, 'addmoney.html', {'hesapno': hesapno})




# Para çekme sayfasına yönlendiren verilen hesap numarasını yönlendirildiği method
def takemoney(request):
    hesapno = request.POST.get("hesapno")
    return render(request, 'takemoney.html', {'hesapno': hesapno})



#Profile sayfasına yönlendiren ve profil bilgilerini sayfaya gönderen method
def profile(request):
    user = request.user
    current_user = request.user

    balance = Decimal(0)
    tcID = None
    name = None
    lastname = None
    customerID = None
    birthdate = None

    profile_ = None
    try:

        kisi = Tblkisi.objects.filter(tckimlikno=current_user).first()
        musteri = Tblmusteri.objects.filter(tckimlikno=kisi).first()
        accounts = Tblhesap.objects.filter(
            musterino=musteri, hesapaktivasyon=True)

        for acc in accounts:
            balance += acc.hesapbakiye

        profile_ = {
            'tcID': kisi.tckimlikno,
            'name': kisi.ad,
            'lastname': kisi.soyad,
            'birthdate': str(kisi.dogumtarihi),
            'customerID': musteri.musterino,
            'balance': balance,
        }
    except:
        pass

    return render(request, 'profile.html', {'profile': profile_})






## Havale sayfasına yönlendiren ve gerekli hesap bilgilerini gönderen method
def transfer(request):
    current_user = request.user
    try:
        kisi = Tblkisi.objects.filter(tckimlikno=current_user).first()
        musteri = Tblmusteri.objects.filter(tckimlikno=kisi).first()
        accounts = Tblhesap.objects.filter(
            musterino=musteri, hesapaktivasyon=True)

    except:
        pass
    return render(request, 'transfer.html', {'accounts': accounts})




## Müşteriye ait tüm hesapları(aktif olan) database den çeken ve 
## hesaplar sayfasına yönlendirildiği method
def accounts(request):
    current_user = request.user
    accounts = None
    try:
        kisi = Tblkisi.objects.filter(tckimlikno=current_user).first()
        musteri = Tblmusteri.objects.filter(tckimlikno=kisi).first()
        accounts = Tblhesap.objects.filter(
            musterino=musteri, hesapaktivasyon=True)

    except:
        pass
    return render(request, 'accounts.html', {'accounts': accounts})






## Müşterinin giriş yaptığı(TC kimlik numarası ile) ve kontrollerin yapıldığı method
def signin(request):

    if request.method == "GET":
        return redirect("/login")
    else:
        tcNo = request.POST.get("tcNo")
        kisi = Tblkisi.objects.filter(tckimlikno=tcNo).first()
        musteri = Tblmusteri.objects.filter(tckimlikno=kisi).first()

        print(musteri.musteriaktivaston)
        if not musteri.musteriaktivaston:
            messages.success(request, "Account has been disabled!")
            return redirect(request.POST.get('next', '/login'))

        password = request.POST.get("password")
        # User login start
        user = authenticate(username=tcNo, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You are now logged in!")
            else:
                messages.warning(request, "Account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            messages.warning(
                request, "The username and password were incorrect.")
        # User login end

        return redirect(request.POST.get('next', '/'))






## Müşterinin kayıt olduğu ve müşterinin tc kimlik numarasına ait bir banka hesabı
#olduğu kontrol ediliyor.
def signup(request):
    if request.method == "GET":
        return redirect("/login")

    tcNo = request.POST.get("tcNo")
    password = request.POST.get("password")
    name = request.POST.get("name")
    lastname = request.POST.get("lastname")
    birthday = request.POST.get("birthday")

    try:
        person = get_object_or_404(Tblmusteri, tckimlikno=tcNo)
        return HttpResponse("Kullanıcı Zaten Kayıtlıdır.")
    except:
        pass
    newPerson = Tblkisi(tckimlikno=tcNo, ad=name,
                        soyad=lastname, dogumtarihi=birthday)
    newPerson.save()
    # User register start
    user = User.objects.create_user(tcNo, '', password)
    user.firs_name = name
    user.last_name = lastname
    user.is_active = True
    user.save()
    # User register end

    number_ms = 000000000
    try:
        while True:
            number_ms = randrange(100000000, 999999999)
            musteri__ = get_object_or_404(Tblmusteri, musterino=number_ms)
    except:
        print("Müşteri Yok.")
        pass

    # TODO musteri numarası oluşturucu
    newClient = Tblmusteri(musterino=number_ms, tckimlikno=newPerson,
                           musterisifre=password, musteriaktivaston=True)

    newClient.save()
    # TODO ana sayfaya yönlendirme ve bilgi aktarma
    return render(request, "login.html")







## Profilin güncellendiği ve tekrar profile sayfasına yönlendildiği method.
def profileupdate(request):
    tcNo = request.POST.get("tcNo")
    name = request.POST.get("name")
    lastname = request.POST.get("lastname")
    birthdate = request.POST.get("birthdate")

    try:
        kisi = Tblkisi.objects.filter(tckimlikno=tcNo).first()

        kisi.ad = name
        kisi.soyad = lastname
        #date = datetime.strptime(birthdate, '%Y-%m-%d')
        kisi.dogumtarihi = birthdate
        kisi.save()
        messages.success(request, "Profile updated!")
    except Exception as e:
        print(e)
        messages.success(request, "Profile is not updated!")
    return redirect("/profile")





##Profilin(Banka hesabının) silindiği(inactive) yapıldığı method.
def profiledelete(request):
    tcNo = request.POST.get("tcNo")
    birthdate = request.POST.get("birthdate")

    try:
        kisi = Tblkisi.objects.filter(tckimlikno=tcNo).first()
        musteri = Tblmusteri.objects.all().filter(tckimlikno=kisi).first()

        musteri.musteriaktivaston = False
        musteri.save()

        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        messages.success(request, "Profile Deleted!")
    except:
        messages.success(request, "Profile is not Deleted! Somethinds Wrong!")
    return redirect(request.POST.get('next', '/'))





##Şifrenin güncellendiği ve tekrardan giriş yapıldığı method.
def passwordupdate(request):
    user = request.user
    oldpassword = request.POST.get("oldpassword")
    oldpasswordconfirm = request.POST.get("oldpasswordconfirm")
    newpassword = request.POST.get("newpassword")

    if not oldpassword == oldpasswordconfirm:
        messages.success(request, "Confirm Password Is Not Equal To Password!")
        return redirect(request.POST.get('next', '/'))

    try:
        kisi = Tblkisi.objects.all().filter(tckimlikno = user).first()
        musteri = Tblmusteri.objects.all().filter(tckimlikno= kisi).first()

        if not musteri.musterisifre == oldpassword:
            messages.success(request, "Password is Wrong!")
            return redirect(request.POST.get('next', '/'))

        musteri.musterisifre = newpassword
        musteri.save()

        user.set_password(newpassword)
        user.save()
        login(request, user)
        messages.success(request, "Password is Updated!")

    except:
        messages.success(request, "Someting is Wrong!")
        return redirect(request.POST.get('next', '/'))

    return redirect(request.POST.get('next', '/profile'))







## Hesap eklediğiniz method
def addaccount(request):
    if request.method == "GET":
        return redirect("/")
    current_client = request.user
    hesapekno = 0000
    musteri = None
    try:
        kisi = Tblkisi.objects.all().filter(tckimlikno=current_client).first()
        musteri = Tblmusteri.objects.all().filter(tckimlikno=kisi).first()
        accs = Tblhesapek.objects.filter(musterino=musteri)
        acc = accs.order_by('-hesapekno').first()
        hesapekno = int(acc.hesapekno) + 1

    except:
        hesapekno = 1000

    hesapno = str(hesapekno)+str(musteri.musterino)

    account = Tblhesap(hesapno=hesapno, musterino=musteri, hesapbakiye=0,
                       hesaptarihi=timezone.now(), hesapaktivasyon=True)
    account.save()

    account_pl = Tblhesapek(
        musterino=musteri, hesapekno=hesapekno, hesapno=account)
    account_pl.save()
    messages.success(request, "Account added!")
    return redirect("/accounts")




## Çıkış yapılan metod

def logoutpage(request):
    if not request.user.is_authenticated:
        return redirect('/')
    logout(request)
    messages.success(request, "You are now logged out!")
    return redirect('/')





### Hesap bakiyesine para eklenilen hesap
def addmoneytobalance(request):
    hesapno = request.POST.get("hesapno")
    amount = request.POST.get("amount")

    try:
        hesap = Tblhesap.objects.all().filter(hesapno=hesapno).first()
        hesapbakiyesi = hesap.hesapbakiye
        hesap.hesapbakiye = Decimal(amount) + Decimal(hesapbakiyesi)
        hesap.save()
        messages.success(
            request, "Your money is added your account. Spend for Happy Days!")

    except:
        return HttpResponse("There isn't account you have. Please! Return and try again.")

    return redirect("/accounts")





## Hesap bakiyesinden para çekilen method
def takemoneyfrombalance(request):
    hesapno = request.POST.get("hesapno")
    amount = Decimal(request.POST.get("amount"))

    try:
        hesap = Tblhesap.objects.all().filter(hesapno=hesapno).first()
        hesapbakiyesi = Decimal(hesap.hesapbakiye)

        if amount > hesapbakiyesi:
            messages.success(
                request, "insufficient balance. Please try again!")
            return redirect("/takemoney")
        hesapbakiyesi = hesapbakiyesi - amount
        hesap.hesapbakiye = hesapbakiyesi
        hesap.save()
        messages.success(
            request, "Process is completed. Spend for Happy Days!")

    except:
        return HttpResponse("There isn't account you have. Please! Return and try again.")

    return redirect("/accounts")






##Hesabın silindiği(inactive) edildiği metot
def deleteaccount(request):
    hesapno = request.POST.get("hesapno")
    try:
        hesap = Tblhesap.objects.all().filter(hesapno=hesapno).first()
        if hesap.hesapbakiye != 0:
            messages.success(
                request, "Your account isn t deleted! Because your balance isn t 0. You have money in your account. Please take your money and try again!")
            return redirect("/accounts")

        hesap.hesapaktivasyon = False
        hesap.save()
        messages.success(request, "Your account is deleted!")

    except:
        return HttpResponse("There isn't account you have. Please! Return and try again.")

    return redirect("/accounts")






## Hesaba ait havale işlemlerinin veri tabanından çekildiği ve transaction sayfasına yön-
## lendirildiği metod.
def getaccounttransactions(request):
    hesapno = request.POST.get("hesapno")

    try:
        account = Tblhesap.objects.all().filter(hesapno=hesapno).first()
        getReceiverTransc = Havale.objects.all().filter(
            alicihesapno=account).order_by("-havaletarihi")
        getSenderTransc = Havale.objects.all().filter(
            gondericihesapno=hesapno).order_by("-havaletarihi")

        trans = getReceiverTransc | getSenderTransc
        print(trans)
        trans.order_by("-havaletarihi")

        if not getSenderTransc and not getReceiverTransc:
            messages.success(request, "This account has not any transactions.")
            return redirect("/accounts")

    except:
        pass
    return render(request, "accounttransactions.html", {'hesapno': hesapno, 'accounttransactions': trans})






### Havale işlemlerin yapıldığı(Hem virman hem müşteriler arası)
def sendmoney(request):
    senderaccountNo = request.POST.get("senderaccount")
    receiveraccountNo = request.POST.get("receiveraccount")
    moneyamount = Decimal(request.POST.get("moneyamount"))
    havaletipno = request.POST.get("havaletipno")

    try:
        senderaccount = Tblhesap.objects.all().filter(hesapno=senderaccountNo).first()
        senderhesapbakiye = Decimal(senderaccount.hesapbakiye)

        if moneyamount > senderhesapbakiye:
            messages.success(
                request, "insufficient balance. Please try again!")
            return redirect("/transfer")

        receiveraccount = Tblhesap.objects.all().filter(
            hesapno=receiveraccountNo).first()
        receiverhesapbakiye = Decimal(receiveraccount.hesapbakiye)

        senderhesapbakiye = senderhesapbakiye - moneyamount
        receiverhesapbakiye = receiverhesapbakiye + moneyamount

        senderaccount.hesapbakiye = senderhesapbakiye
        receiveraccount.hesapbakiye = receiverhesapbakiye

        havaletip = Tblhavaletip.objects.all().filter(
            havaletipno=int(havaletipno)).first()
        number_hn = 00000000000
        try:
            while True:
                number_hn = randrange(10000000000, 99999999999)
                havale_ = get_object_or_404(Havale, havaletipno=number_hn)
        except:
            pass
        havale = Havale(havaleno=str(number_hn), gondericihesapno=senderaccountNo, alicihesapno=receiveraccount,
                        havaletipno=havaletip, havalemiktari=moneyamount, havaletarihi=timezone.now())

        senderaccount.save()
        receiveraccount.save()
        havale.save()
        messages.success(
            request, "Process Is Completed! Have Nice Day!")
    except Exception as inst:
        messages.success(
            request, "Sometings Wrong! Pleas Try Again!")
        return redirect("/transfer")
    return redirect("/transfer")



## Anlık kullanıcı bilgisi //// TEST için yazılımıştır.
def get_user(request):
    current_user = request.user
    kisi = Tblkisi.objects.filter(tckimlikno=current_user).first()
    musteri = Tblmusteri.objects.filter(tckimlikno=kisi).first()
    hesapekler = Tblhesapek.objects.all()
    print(hesapekler)
    print(kisi)
    print(musteri)
    print(current_user.username)
    return render_to_response({})





### HGS servisinden hgs ürünlerinin çekildiği ve hgs sayfasında gösterildiği metod
def gethgsproducts(request):
    req = urllib.request.urlopen('http://127.0.0.1:8002/gethgsproduct')
    
    current_user = request.user
    accounts = None
    try:
        kisi = Tblkisi.objects.filter(tckimlikno=current_user).first()
        musteri = Tblmusteri.objects.filter(tckimlikno=kisi).first()
        accounts = Tblhesap.objects.filter(
            musterino=musteri, hesapaktivasyon=True)

    except:
        pass
    
    data = json.loads(req.read().decode(req.info().get_param('charset') or 'utf-8'))
    return render(request, "hgsbuy.html", {'datas': data, 'accounts': accounts})


### HGS ürünün satın alındığı, hesap bakiyesinden düşürüldüğü ve servis tarafından 
## ürünün kaldırıldığı metot
@csrf_exempt
def buyhgsproducts(request):

    post_data = {'data': request.POST.get("pk")}
    amount = Decimal(request.POST.get("fiyat"))
    
    hesapno = request.POST.get("account")
    
    try:
        account = Tblhesap.objects.filter(hesapno=hesapno, hesapaktivasyon=True).first()
        print(account)
        hesapbakiye =  Decimal(account.hesapbakiye)
        
        if amount > hesapbakiye:
            messages.success(
                request, "insufficient balance. Please try again!")
            return redirect("/gethgsproducts")
        hesapbakiye = hesapbakiye - amount
        
        account.hesapbakiye = hesapbakiye
        account.save()

        response = requests.post("http://127.0.0.1:8002/buyhgsproduct", data=post_data)

        messages.success(request, "Processs is Completed!")
    except:
        pass
    

    return redirect(request.POST.get('next', '/gethgsproducts'))
    


