# Generated by Django 4.0.4 on 2022-04-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
        ('exams', '0002_alter_examcategory_name_alter_mainexam_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='examcategory',
            name='subjects',
            field=models.ManyToManyField(related_name='exam_categories', to='subjects.subject'),
        ),
    ]