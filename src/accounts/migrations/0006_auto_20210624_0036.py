# Generated by Django 3.0.8 on 2021-06-23 19:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210623_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='submission_code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student_assignments',
            name='published_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 24, 0, 36, 33, 383443)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submission_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 24, 0, 36, 33, 385437)),
        ),
    ]
