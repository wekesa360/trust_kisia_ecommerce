import uuid
from django.db import models
from autoslug import AutoSlugField
from PIL import Image
from io import BytesIO
from django.urls import reverse
from django.core.files import File
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=False, blank=False)
    sub_category = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from=lambda instance: instance.category_name, 
                         slugify=lambda value: value.replace(' ', '-'))
    
    def __str__(self) -> str:
        return self.sub_category
    
    class Meta:
        db_table = 'categories'
    

class Product(models.Model):
    TAGS_CHOICES = (
        ('Hot Sale', 'Hot Sale'),
        ('Featured', 'Featured'),
        ('Latest Products', 'Latest Products')
    )
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, blank=False, unique=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField()
    tag = models.CharField(max_length=100, choices=TAGS_CHOICES, blank=True)
    slug = AutoSlugField(populate_from=lambda instance: instance.name,
                         slugify=lambda value: value.replace(' ', '-'))
    quantity = models.IntegerField()
    thumbnail = models.FileField(upload_to='product_images/', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    product_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            return ''
        
    def get_add_to_cart_url(self):
        return reverse('shop:add-to-cart', kwargs={'slug': self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse('shop:remove-from-cart', kwargs={'slug': self.slug})
    
    def make_thumbnail(self, image_file, size=(50, 50)):
        img = Image.open(image_file)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=90)
        
        thumbnail = File(thumb_io, name=image_file.name)
        
        return thumbnail
    
    
    class Meta:
        db_table = 'products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=False, unique=False, on_delete=models.CASCADE)
    image = models.FileField(upload_to='product_image/', blank=True)
    
    def __str__(self) -> str:
        return self.product.name
    
    def get_absolute_url(self):
        return 'http://127.0.0.1:8000' + self.image.url
    
    class Meta:
        db_table = 'product_images'



class DeliveryCharges(models.Model):
    county = models.CharField(max_length=256)
    specific_pickup_point = models.CharField(max_length=256)
    fee = models.PositiveBigIntegerField()
    
    def __str__(self):
        return self.specific_pickup_point
    
    class Meta:
        db_table = 'shipping_charges'


class OrderItem(models.Model):
    ordered = models.BooleanField()
    product = models.ForeignKey(Product, blank=False, unique=False, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_discount_item_price(self):
        return self.quantity * self.product.discount
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()
    
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()
    
    class Meta:
        db_table = 'order_items'


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    PAYMENT_CHOICES = (
        
    )
    products = models.ManyToManyField(OrderItem)
    payment = models.CharField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending', blank=True)
    delivery_address = models.ForeignKey(DeliveryCharges, blank=False, unique=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    
    def get_total_price(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price() 
        return total + self.delivery_address.fee

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'orders'


class Customer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        full_name = f'{self.first_name}  {self.last_name}'
        return full_name


    class Meta:
        db_table = 'customer_details'


