# Generated by Django 4.2.4 on 2023-09-22 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relation',
            name='item',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='user',
        ),
        migrations.RemoveField(
            model_name='review',
            name='item',
        ),
        migrations.RemoveField(
            model_name='review',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
    ]