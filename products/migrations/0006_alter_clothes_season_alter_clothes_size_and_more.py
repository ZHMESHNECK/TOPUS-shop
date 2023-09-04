# Generated by Django 4.2.4 on 2023-09-01 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_gallery_cloth_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='season',
            field=models.CharField(blank=True, choices=[('ALL_SEASON', 'Все сезон'), ('SUMMER', 'Літо'), ('AUTUM', 'Осінь'), ('WINTER', 'Зима'), ('SPRING', 'Весна')], default='-', max_length=11, verbose_name='Сезон'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clothes',
            name='size',
            field=models.CharField(blank=True, choices=[('-', '-'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], default='-', max_length=2, verbose_name='Розмір'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gaming',
            name='color',
            field=models.CharField(blank=True, default='1', max_length=15, verbose_name='Колір'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gaming',
            name='model',
            field=models.CharField(blank=True, default='1', max_length=50, verbose_name='Модель'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='home',
            name='color',
            field=models.CharField(blank=True, default='1', max_length=15, verbose_name='Колір'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='home',
            name='material',
            field=models.CharField(blank=True, default='-', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mainmodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='mainmodel',
            name='description',
            field=models.TextField(blank=True, default='1', verbose_name='Опис'),
            preserve_default=False,
        ),
    ]
