# Generated by Django 5.1.3 on 2024-11-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
