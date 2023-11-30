# Generated by Django 4.2.7 on 2023-11-30 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='tenant',
            field=models.CharField(choices=[('O', 'Offen'), ('T', 'Vergeben'), ('W', 'In Arbeit'), ('C', 'Komplett'), ('A', 'Abgebrochen')], default='O', max_length=1),
        ),
    ]