from django.db import models

# Create your models here.


class Tblhgs(models.Model):
    tckimlikno = models.CharField(primary_key=True, max_length=11)
    ad = models.CharField(max_length=50, blank=True, null=True)
    soyad = models.CharField(max_length=50, blank=True, null=True)
    bakiye = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    hgsno = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tblhgs'


class Tblhgsurun(models.Model):
    hgsno = models.CharField(primary_key=True, max_length=11)
    price = models.DecimalField(max_digits=18, decimal_places=3, blank=True, null=True)
    sinif = models.CharField(max_length=50, blank=True, null=True)
    aractipi = models.CharField(max_length=50, blank=True, null=True)
    aciklama = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblHgsUrun'