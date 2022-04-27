# Generated by Django 4.0.4 on 2022-04-27 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subjects', '0001_initial'),
        ('exams', '0004_alter_examcategory_subjects'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('opening_date', models.DateField()),
                ('closing_date', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batches_created', to=settings.AUTH_USER_MODEL)),
                ('exam_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='exams.examcategory')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batches_modified', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(related_name='batches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BatchTiming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_timings', to='batches.batch')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_timings', to='subjects.subject')),
            ],
        ),
    ]
