# Generated by Django 3.2.7 on 2021-10-02 00:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('listing_title', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d')),
                ('review', models.TextField(blank=True)),
                ('review_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
