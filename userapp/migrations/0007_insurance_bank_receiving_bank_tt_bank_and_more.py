# Generated by Django 4.1.5 on 2023-01-30 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0006_alter_company_trader'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance_bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Receiving_bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Tt_bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='insurance_bank',
        ),
        migrations.RemoveField(
            model_name='company',
            name='receiving_bank',
        ),
        migrations.RemoveField(
            model_name='company',
            name='tt_bank',
        ),
        migrations.AddField(
            model_name='company',
            name='insurance_bank',
            field=models.ManyToManyField(to='userapp.insurance_bank'),
        ),
        migrations.AddField(
            model_name='company',
            name='receiving_bank',
            field=models.ManyToManyField(to='userapp.receiving_bank'),
        ),
        migrations.AddField(
            model_name='company',
            name='tt_bank',
            field=models.ManyToManyField(to='userapp.tt_bank'),
        ),
    ]
