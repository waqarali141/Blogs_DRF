# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-02 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
