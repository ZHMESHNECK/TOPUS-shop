# Generated by Django 4.2.4 on 2023-09-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_mainmodel_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainmodel',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2, null=True, verbose_name='Рейтинг'),
        ),
    ]
