# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pv', '0004_auto_20170915_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='PVMeetingDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
