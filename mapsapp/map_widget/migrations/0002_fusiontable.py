# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-05 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_widget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FusionTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.TextField()),
            ],
        ),
    ]