# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pv', '0018_pvmeetingappointment_special_conditions'),
    ]

    operations = [
        migrations.AddField(
            model_name='pvuserinfo',
            name='approved_by_virtual_meeting',
            field=models.BooleanField(default=False, verbose_name='Approved by virtual meeting'),
        ),
    ]
