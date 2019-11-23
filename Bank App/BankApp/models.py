from django.db import models

# Create your models here.


#Havale tablosu ile bağlantı kurulan ve ekleme, güncelleme ve silme işlemleri için kullandığımız
#metod
class Havale(models.Model):
    havaleno = models.CharField(db_column='HavaleNo', primary_key=True, max_length=11)  # Field name made lowercase.
    gondericihesapno = models.CharField(db_column='GondericiHesapNo', max_length=15, blank=True, null=True)  # Field name made lowercase.
    alicihesapno = models.ForeignKey('Tblhesap', models.DO_NOTHING, db_column='AliciHesapNo', blank=True, null=True)  # Field name made lowercase.
    havaletipno = models.ForeignKey('Tblhavaletip', models.DO_NOTHING, db_column='HavaleTipNo', blank=True, null=True)  # Field name made lowercase.
    havalemiktari = models.DecimalField(db_column='HavaleMiktari', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    havaletarihi = models.DateTimeField(db_column='HavaleTarihi', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.havaleno

    class Meta:
        managed = False
        db_table = 'Havale'

#HavaleTip tablosu ile bağlantı kurulan ve ekleme, güncelleme ve silme işlemleri için kullandığımız
#metod
class Tblhavaletip(models.Model):
    havaletipno = models.IntegerField(db_column='HavaleTipNo', primary_key=True)  # Field name made lowercase.
    havaleisim = models.CharField(db_column='HavaleIsim', max_length=50, blank=True, null=True)  # Field name made lowercase.
    islemucreti = models.DecimalField(db_column='IslemUcreti', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.havaleisim
    class Meta:
        managed = False
        db_table = 'tblHavaleTip'

#Hesap tablosu ile bağlantı kurulan ve ekleme, güncelleme ve silme işlemleri için kullandığımız
#metod
class Tblhesap(models.Model):
    hesapno = models.CharField(db_column='HesapNo', primary_key=True, max_length=15)  # Field name made lowercase.
    musterino = models.ForeignKey('Tblmusteri', models.DO_NOTHING, db_column='MusteriNo', blank=True, null=True)  # Field name made lowercase.
    hesapbakiye = models.DecimalField(db_column='HesapBakiye', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    hesaptarihi = models.DateTimeField(db_column='HesapTarihi', blank=True, null=True)  # Field name made lowercase.
    hesapaktivasyon = models.BooleanField(db_column='HesapAktivasyon', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.hesapno

    class Meta:
        managed = False
        db_table = 'tblHesap'

#Hesap Ek tablosu ile bağlantı kurulan ve ekleme, güncelleme ve silme işlemleri için kullandığımız
#metod
class Tblhesapek(models.Model):
    musterino = models.ForeignKey('Tblmusteri', models.DO_NOTHING, db_column='musteriNo', blank=True, null=True)  # Field name made lowercase.
    hesapekno = models.CharField(db_column='hesapEkNo', max_length=4, blank=True, null=True)  # Field name made lowercase.
    hesapno = models.ForeignKey(Tblhesap, models.DO_NOTHING, db_column='hesapNo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.hesapno

    class Meta:
        managed = False
        db_table = 'tblHesapEk'

#Kişi tablosu ile bağlantı kurulan ve ekleme, güncelleme ve silme işlemleri için kullandığımız
#metod
class Tblkisi(models.Model):
    tckimlikno = models.CharField(db_column='TcKimlikNo', primary_key=True, max_length=11)  # Field name made lowercase.
    ad = models.CharField(db_column='Ad', max_length=50, blank=True, null=True)  # Field name made lowercase.
    soyad = models.CharField(db_column='Soyad', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dogumtarihi = models.DateTimeField(db_column='DogumTarihi', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.tckimlikno

    class Meta:
        managed = False
        db_table = 'tblKisi'

#Müşteri tablosu ile bağlantı kurulan ve ekleme, güncelleme ve silme işlemleri için kullandığımız
#metod
class Tblmusteri(models.Model):
    musterino = models.CharField(db_column='MusteriNo', primary_key=True, max_length=9)  # Field name made lowercase.
    tckimlikno = models.ForeignKey(Tblkisi, models.DO_NOTHING, db_column='TCKimlikNo')  # Field name made lowercase.
    musterisifre = models.CharField(db_column='MusteriSifre', max_length=255)  # Field name made lowercase.
    musteriaktivaston = models.BooleanField(db_column='MusteriAktivaston', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.musterino

    class Meta:
        managed = False
        db_table = 'tblMusteri'
