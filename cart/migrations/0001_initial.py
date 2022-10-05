# Generated by Django 4.0.8 on 2022-10-05 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=140)),
                ('quantity', models.FloatField()),
                ('price', models.FloatField()),
            ],
        ),
    ]
