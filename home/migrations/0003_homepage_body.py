# Generated by Django 4.2.7 on 2023-11-27 19:03

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.RichTextField(default='Test'),
            preserve_default=False,
        ),
    ]