# Generated by Django 4.0.8 on 2022-10-09 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cartproduct_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='date_added',
        ),
    ]
