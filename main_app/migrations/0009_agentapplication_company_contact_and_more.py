# Generated by Django 5.1.3 on 2024-11-29 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_customuser_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentapplication',
            name='company_contact',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='agentapplication',
            name='company_email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='company_contact',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='company_email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='npwp',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.MinLengthValidator(16, message='NPWP must be exactly 16 characters.')]),
        ),
    ]