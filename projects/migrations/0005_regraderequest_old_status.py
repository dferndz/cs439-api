# Generated by Django 3.2.10 on 2022-01-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_regraderequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='regraderequest',
            name='old_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Grade increased', 'Increase'), ('Grade did not change', 'No Change')], default='Pending', max_length=512),
        ),
    ]
