# Generated by Django 2.1.13 on 2019-11-13 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGSAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tblhgsurun',
            fields=[
                ('hgsno', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=18, null=True)),
                ('sinif', models.CharField(blank=True, max_length=50, null=True)),
                ('aractipi', models.CharField(blank=True, max_length=50, null=True)),
                ('aciklama', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tblHgsUrun',
                'managed': False,
            },
        ),
    ]