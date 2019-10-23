# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-23 18:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_timestamp', models.DateTimeField(blank=True, null=True)),
                ('updated_timestamp', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('creation_timestamp', models.DateTimeField(blank=True, null=True)),
                ('updated_timestamp', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=40)),
                ('middle_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('phone_number', models.CharField(max_length=10, null=True)),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('company_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
