# Generated by Django 2.1.13 on 2019-10-26 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Havale',
            fields=[
                ('havaleno', models.CharField(db_column='HavaleNo', max_length=11, primary_key=True, serialize=False)),
                ('gondericihesapno', models.CharField(blank=True, db_column='GondericiHesapNo', max_length=15, null=True)),
                ('havalemiktari', models.DecimalField(blank=True, db_column='HavaleMiktari', decimal_places=2, max_digits=18, null=True)),
                ('havaletarihi', models.DateTimeField(blank=True, db_column='HavaleTarihi', null=True)),
            ],
            options={
                'db_table': 'Havale',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblhavaletip',
            fields=[
                ('havaletipno', models.IntegerField(db_column='HavaleTipNo', primary_key=True, serialize=False)),
                ('havaleisim', models.CharField(blank=True, db_column='HavaleIsim', max_length=50, null=True)),
                ('islemucreti', models.DecimalField(blank=True, db_column='IslemUcreti', decimal_places=0, max_digits=18, null=True)),
            ],
            options={
                'db_table': 'tblHavaleTip',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblhesap',
            fields=[
                ('hesapno', models.CharField(db_column='HesapNo', max_length=15, primary_key=True, serialize=False)),
                ('hesapbakiye', models.DecimalField(blank=True, db_column='HesapBakiye', decimal_places=2, max_digits=18, null=True)),
                ('hesaptarihi', models.DateTimeField(blank=True, db_column='HesapTarihi', null=True)),
                ('hesapaktivasyon', models.BooleanField(blank=True, db_column='HesapAktivasyon', null=True)),
            ],
            options={
                'db_table': 'tblHesap',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblhesapek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hesapekno', models.CharField(blank=True, db_column='hesapEkNo', max_length=4, null=True)),
            ],
            options={
                'db_table': 'tblHesapEk',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblkisi',
            fields=[
                ('tckimlikno', models.CharField(db_column='TcKimlikNo', max_length=11, primary_key=True, serialize=False)),
                ('ad', models.CharField(blank=True, db_column='Ad', max_length=50, null=True)),
                ('soyad', models.CharField(blank=True, db_column='Soyad', max_length=50, null=True)),
                ('dogumtarihi', models.DateTimeField(blank=True, db_column='DogumTarihi', null=True)),
            ],
            options={
                'db_table': 'tblKisi',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblmusteri',
            fields=[
                ('musterino', models.CharField(db_column='MusteriNo', max_length=9, primary_key=True, serialize=False)),
                ('musterisifre', models.CharField(db_column='MusteriSifre', max_length=255)),
                ('musteriaktivaston', models.BooleanField(blank=True, db_column='MusteriAktivaston', null=True)),
            ],
            options={
                'db_table': 'tblMusteri',
                'managed': False,
            },
        ),
    ]