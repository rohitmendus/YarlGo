# Generated by Django 4.0.4 on 2022-05-05 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_test_batch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='dsitributions',
            new_name='distributions',
        ),
    ]
