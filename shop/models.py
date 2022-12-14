import uuid
from django.db import models
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.urls import reverse
from django.core.files import File
from .counties import COUNTIES_CHOICES
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

base_url = 'http://127.0.0.1:8000'
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.category_name}')
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.category_name
    
    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=200, unique=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.category.slug}-{self.sub_category}')
        super(SubCategory, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.sub_category
    
    class Meta:
        db_table = 'sub_categories'  

class Product(models.Model):
    TAGS_CHOICES = (
        ('Hot Sale', 'Hot Sale'),
        ('Featured', 'Featured'),
        ('Latest Products', 'Latest Products')
    )
    name = models.CharField(max_length=200)
    category  = models.ForeignKey(SubCategory, blank=False, unique=False, on_delete=models.CASCADE)
    brand = models.CharField(max_length=256)
    key_features = models.TextField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=0, max_digits=10)
    discount = models.DecimalField(decimal_places=0, max_digits=10)
    tag = models.CharField(max_length=100, choices=TAGS_CHOICES, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    product_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self):
        return f'{base_url}/{self.category.pk}/{self.slug}/'
    
    def get_thumbnail(self):
        if self.thumbnail:
            return f'{base_url}{self.thumbnail.url}'
        else:
            return ''
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    def get_product_image_url(self):
        print(ProductImage.objects.filter(product_id=self.pk).all()[1].image.url)
        url = "{}{}".format(base_url, ProductImage.objects.filter(product_id=self.pk).first().image.url)
        return url
    
    def get_all_product_images(self):
        images = ProductImage.objects.filter(product_id=self.pk).all()
        return images
        
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
    image = models.FileField(upload_to='product_images/', blank=True)
    
    def __str__(self) -> str:
        return self.product.name
    
    def get_absolute_url(self):
        return f'{base_url}{self.image.url}'
    
    class Meta:
        db_table = 'product_images'

class DeliveryCharges(models.Model):
    county = models.CharField(max_length=256, choices=COUNTIES_CHOICES)
    specific_location = models.CharField(max_length=256)
    fee = models.PositiveBigIntegerField()
    
    def __str__(self):
        return f'{self.specific_location}, {self.county} - Ksh. {self.fee}'
    class Meta:
        db_table = 'shipping_charges'


class Customer(models.Model):
    first_name = models.CharField(max_length=80, null=True)
    last_name = models.CharField(max_length=80, null=True)
    phone_number = PhoneNumberField(null=True)
    device = models.CharField(max_length=256, unique=False)
    email = models.EmailField(null=True)
    ordered = models.BooleanField(default=False)
    delivery_address = models.ForeignKey(DeliveryCharges, on_delete=models.DO_NOTHING, default=1)
    # delivery_address = models.CharField(max_length=80, blank=False, unique=False, null=True)
    
    def __str__(self) -> str:
        full_name = f'{self.first_name}  {self.last_name}'
        return full_name


    class Meta:
        db_table = 'customer_details'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, blank=False, unique=False, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    customer = models.ForeignKey(Customer, blank=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_discount_item_price(self):
        return self.quantity * self.product.discount
    
    def get_total_with_discount(self):
        return self.get_total_item_price() - self.get_discount_item_price()
    
    def get_final_price(self):
        if self.product.discount:
            return self.get_total_with_discount()
        return self.get_total_item_price()
    
    def if_in_stock(self):
        if self.quantity < self.product.quantity:
            return True
        return False
           
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem, related_name='products')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending', blank=True)
    ordered_date = models.DateField()
    ordered= models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True, editable=False)
    
    def get_total_price(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        return total # + self.customer.delivery_address.fee

    def __str__(self):
        username = f'{self.customer.first_name} {self.customer.last_name} - Order id: {self.uuid}'
        return username
    
    def get_total_no_items(self):
        count = 0
        for order_item in self.products.all():
            count += order_item.quantity
        return count
    
    
    class Meta:
        db_table = 'orders'


class EmailDispatch(models.Model):
    email = models.TextField()
    name = models.CharField(max_length=256)
    subject = models.CharField(max_length=526)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email


    class Meta:
        db_table = 'email_dispatches'

class ProcessOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cancel_order = models.BooleanField(default=False)
    total_charges = models.PositiveIntegerField(default=0, blank=True)
    payment_transacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.order.uuid}'
    
    class Meta:
        db_table = 'process_orders'

class CancelledOrder(models.Model):
    customer_name = models.CharField(max_length=256)
    customer_email = models.EmailField()
    order_id = models.CharField(max_length=100)
    products_order = models.TextField()
    order_cancelled = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

    
    class Meta:
        db_table = 'cancelled_orders'

