# Generated by Django 4.2.4 on 2023-12-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_clothes_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainmodel',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2, null=True, verbose_name='Рейтинг'),
        ),
    ]