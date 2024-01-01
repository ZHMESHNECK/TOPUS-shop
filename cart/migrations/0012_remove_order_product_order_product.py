# Generated by Django 4.2.4 on 2023-12-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_mainmodel_rating'),
        ('cart', '0011_alter_order_how_to_pay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='adress',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='item_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(
                to='products.mainmodel', verbose_name='Товар'),
        ),
    ]
