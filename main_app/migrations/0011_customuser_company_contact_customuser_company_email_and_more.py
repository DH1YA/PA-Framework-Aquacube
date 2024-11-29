# Generated by Django 5.1.3 on 2024-11-29 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_remove_customuser_company_contact_and_more'),
    ]

    operations = [
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
            model_name='agentapplication',
            name='company_contact',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='agentapplication',
            name='company_email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
