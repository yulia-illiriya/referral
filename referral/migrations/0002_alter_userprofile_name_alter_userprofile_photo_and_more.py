# Generated by Django 4.2.4 on 2023-08-09 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Surname'),
        ),
    ]
