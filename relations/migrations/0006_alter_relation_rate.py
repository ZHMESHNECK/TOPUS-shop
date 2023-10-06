# Generated by Django 4.2.4 on 2023-10-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0005_alter_relation_parent_alter_relation_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='rate',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=None, null=True, verbose_name='Оцінка'),
        ),
    ]
