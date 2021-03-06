# Generated by Django 4.0.4 on 2022-04-26 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
        ('exams', '0003_examcategory_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examcategory',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='exam_categories', to='subjects.subject'),
        ),
    ]
