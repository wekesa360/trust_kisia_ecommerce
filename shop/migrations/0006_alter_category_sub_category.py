# Generated by Django 4.1 on 2022-10-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_category_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.CharField(max_length=200),
        ),
    ]
