# Generated by Django 3.2.10 on 2022-01-18 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='url',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
