# Generated by Django 4.1.5 on 2023-01-17 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_company_type_remove_company_company_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='counterparty_onboard_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='company',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='company',
            name='product',
        ),
        migrations.AlterField(
            model_name='company',
            name='serenity_onboard_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='payment',
            field=models.ManyToManyField(to='userapp.payment'),
        ),
        migrations.AddField(
            model_name='company',
            name='product',
            field=models.ManyToManyField(to='userapp.product'),
        ),
    ]