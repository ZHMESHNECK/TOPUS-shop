# Generated by Django 4.2.4 on 2023-12-04 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_profile_adress_alter_profile_department'),
        ('cart', '0009_remove_order_number_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Вартість'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer', verbose_name='Замовник'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Прийнято', 'Прийнято'), ('Збирається', 'Збирається'), ('Відправлено', 'Відправлено'), ('Готове до видачі', 'Готове до видачі'), ('Виконане', 'Виконане'), ('Відмінено', 'Відмінено')], default='Прийнято', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='summ_of_pay',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Всього'),
        ),
    ]