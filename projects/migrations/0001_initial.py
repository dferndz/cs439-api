# Generated by Django 3.2.9 on 2021-12-16 23:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=512)),
                ('description', models.CharField(max_length=512)),
                ('info_site_name', models.CharField(max_length=512)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
