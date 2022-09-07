# Generated by Django 4.1 on 2022-09-07 15:20

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
                ('sub_category', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80, null=True)),
                ('last_name', models.CharField(max_length=80, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('device', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('delivery_address', models.CharField(max_length=80, null=True)),
            ],
            options={
                'db_table': 'customer_details',
            },
        ),
        migrations.CreateModel(
            name='DeliveryCharges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county', models.CharField(max_length=256)),
                ('specific_pickup_point', models.CharField(max_length=256)),
                ('fee', models.PositiveBigIntegerField()),
            ],
            options={
                'db_table': 'shipping_charges',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tag', models.CharField(blank=True, choices=[('Hot Sale', 'Hot Sale'), ('Featured', 'Featured'), ('Latest Products', 'Latest Products')], max_length=100)),
                ('quantity', models.IntegerField()),
                ('thumbnail', models.FileField(upload_to='product_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, upload_to='product_image/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'db_table': 'product_images',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField()),
                ('quantity', models.IntegerField(default=1)),
                ('ordered_date', models.DateTimeField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField()),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
                ('products', models.ManyToManyField(to='shop.orderitem')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
