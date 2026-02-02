from django.db import models
from myapp.models import Catogory
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('myapp.Catogory', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    def get_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

class Variation_manager(models.Manager):
    def colors(self):
        return super(Variation_manager, self).filter(variation_catogery="color", is_active=True)

    def sizes(self):
        return super(Variation_manager, self).filter(variation_catogery="size", is_active=True)

variation_catagory_choice=(('color','color'),('size','size'),)
    
class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE )
    variation_catogery=models.CharField(max_length=100,choices=variation_catagory_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField( auto_now=True)
    objects=Variation_manager()

    def  __str__(self):
        return self.variation_value
