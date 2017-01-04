# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Conddrugs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cond', models.CharField(unique=True, max_length=20)),
                ('drugs', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='converse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telno', models.CharField(max_length=20, blank=True)),
                ('phonedoctor', models.CharField(max_length=20, blank=True)),
                ('dmsg', models.CharField(max_length=700, blank=True)),
                ('pmsg', models.CharField(max_length=700, blank=True)),
                ('illness', models.CharField(max_length=700, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='convMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mem_phone', models.CharField(max_length=20, blank=True)),
                ('phonedoctor', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diognosis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dname', models.CharField(max_length=40)),
                ('telno', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=30)),
                ('diognosis', models.CharField(max_length=700)),
                ('added', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('page', models.IntegerField()),
                ('email', models.CharField(default=False, max_length=50)),
                ('amb', models.CharField(default=False, max_length=5)),
                ('is_prescribed', models.BooleanField(default=False)),
                ('compill', models.CharField(max_length=700)),
                ('fup', models.CharField(max_length=700)),
                ('reply', models.CharField(max_length=700)),
                ('amt', models.CharField(max_length=30)),
                ('doctortelno', models.CharField(max_length=30)),
                ('illness', models.CharField(max_length=700)),
            ],
        ),
        migrations.CreateModel(
            name='Enterpay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telno', models.CharField(max_length=20)),
                ('amount', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('added', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Illness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('email', models.CharField(max_length=40)),
                ('pname', models.CharField(max_length=50)),
                ('sname', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=30)),
                ('illness', models.CharField(max_length=700)),
                ('kin', models.CharField(max_length=30)),
                ('kintelno', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('page', models.IntegerField()),
                ('amb', models.CharField(default=False, max_length=5)),
                ('amt', models.CharField(default=False, max_length=5)),
                ('doctortelno', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(to='Doct.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Patientr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=20)),
                ('pwd', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fname', models.CharField(default=False, max_length=20, blank=True)),
                ('sname', models.CharField(default=False, max_length=30, blank=True)),
                ('page', models.IntegerField(blank=True)),
                ('gender', models.CharField(default=False, max_length=30, blank=True)),
                ('telno', models.CharField(default=False, max_length=20, blank=True)),
                ('username', models.CharField(default=False, max_length=20, blank=True)),
                ('password', models.CharField(max_length=30)),
                ('email', models.CharField(default=False, max_length=50, blank=True)),
                ('street', models.CharField(default=False, max_length=50, blank=True)),
                ('city', models.CharField(default=False, max_length=20, blank=True)),
                ('state', models.CharField(default=False, max_length=20, blank=True)),
                ('zip_code', models.CharField(default=False, max_length=5, blank=True)),
                ('specialty', models.CharField(default=False, max_length=20)),
                ('role', models.CharField(default=False, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Topup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_sent', models.CharField(max_length=50, verbose_name=b'Airtime')),
                ('receiver_number', models.CharField(max_length=50)),
                ('receiver_fname', models.CharField(max_length=100)),
                ('receiver_lname', models.CharField(max_length=100)),
                ('sender_fullname', models.CharField(max_length=100)),
                ('receiver_country_code', models.CharField(max_length=200)),
                ('added', models.DateTimeField()),
                ('productcode', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('register_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Doct.Register')),
                ('msg', models.CharField(default=False, max_length=20)),
            ],
            bases=('Doct.register',),
        ),
    ]
