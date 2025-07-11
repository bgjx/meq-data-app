# Generated by Django 5.2.3 on 2025-06-26 13:41

import account.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_emailverification_userprofile_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='emailverification',
            name='expires_at',
            field=models.DateTimeField(default=account.models.default_expiry),
        ),
    ]
