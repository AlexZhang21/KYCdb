# Generated by Django 4.1.5 on 2023-01-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='company_type',
        ),
        migrations.AddField(
            model_name='company',
            name='company_type',
            field=models.ManyToManyField(to='userapp.company_type'),
        ),
    ]
