# Generated by Django 4.2.2 on 2023-06-27 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_address_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.IntegerField(null=True),
        ),
    ]