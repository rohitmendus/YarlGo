# Generated by Django 4.0.4 on 2022-05-11 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_rename_dsitributions_test_distributions'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertest',
            name='completed_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 17, 20, 9, 877108)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertest',
            name='started_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 17, 20, 22, 29050)),
            preserve_default=False,
        ),
    ]
