from django.db import models


# Create your models here.
class Catogory(models.Model):
    
    category_name = models.CharField(max_length=100, unique=True)
    slug=models.SlugField(max_length=100 )
    description=models.TextField(max_length=255, blank=True)
    cat_image=models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = 'Catogory'
        verbose_name_plural = 'Catogories'
    def get_url(self):
        return f'/store/{self.slug}/'

    def __str__(self):
        return self.category_name
    

