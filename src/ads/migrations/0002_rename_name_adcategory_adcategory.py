# Generated by Django 5.1.1 on 2024-09-18 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adcategory',
            old_name='name',
            new_name='adCategory',
        ),
    ]
