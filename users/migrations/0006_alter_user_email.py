# Generated by Django 3.2.10 on 2021-12-17 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211217_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
