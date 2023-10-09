# Generated by Django 4.2.4 on 2023-10-06 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('relations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='mainmodel',
            name='viewed',
            field=models.ManyToManyField(related_name='view', through='relations.Relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gallery_home',
            name='home_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.home', verbose_name='home_photo'),
        ),
        migrations.AddField(
            model_name='gallery_gaming',
            name='gaming_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.gaming', verbose_name='gaming_photo'),
        ),
        migrations.AddField(
            model_name='gallery_cloth',
            name='clothes_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.clothes', verbose_name='cloth_photo'),
        ),
    ]
