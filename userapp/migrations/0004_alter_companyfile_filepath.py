# Generated by Django 4.1.5 on 2023-01-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_payment_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyfile',
            name='filepath',
            field=models.FileField(max_length=1000, null=True, upload_to='files/', verbose_name=''),
        ),
    ]
