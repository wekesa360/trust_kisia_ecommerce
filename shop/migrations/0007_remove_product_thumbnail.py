# Generated by Django 4.1 on 2022-09-08 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_order_ordered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='thumbnail',
        ),
    ]
