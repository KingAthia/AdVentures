# Generated by Django 5.1.1 on 2024-09-18 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_rename_name_adcategory_adcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='adCategory',
        ),
        migrations.AddField(
            model_name='ad',
            name='adCategory',
            field=models.ManyToManyField(related_name='ads', to='ads.adcategory'),
        ),
    ]
