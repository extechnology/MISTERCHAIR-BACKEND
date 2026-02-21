from contextlib import nullcontext
from django.template.defaultfilters import default
import PIL.PngImagePlugin
from django.db import models
from tinymce.models import HTMLField
import uuid



class Category(models.Model):
    category_name = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.category_name

class Chair(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    SPECIAL_TAGS = (
        ('New', 'New'),
        ('Bestseller', 'Bestseller'),
        ('Trending', 'Trending'),
        ('Limited', 'Limited')
    )

    name = models.CharField(max_length=255)
    description = HTMLField()

    special_tag = models.CharField(max_length=255, choices=SPECIAL_TAGS, default='New')

    minimum_order_quantity = models.PositiveIntegerField(default=1)
    
    height_stability = models.CharField(max_length=255, null=True, blank=True)
    back_support = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.CharField(max_length=255, null=True, blank=True)

    key_features = HTMLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    

    def __str__(self):
        return self.name


class ChairColors(models.Model):
    chair = models.ForeignKey(Chair, on_delete=models.CASCADE, related_name='chair_colors')
    color_name = models.CharField(max_length=255, help_text="Enter the color name (eg. 'black' or 'white and black')")
    color_code = models.CharField(max_length=255, help_text="Enter the color code in hex format")
    color_code_2 = models.CharField(max_length=255, null=True, blank=True, help_text="Enter the color code in hex format if its is a multicolor")
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    
    if_discount = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    available_stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null = True, blank = True)

    def __str__(self):
        return self.color_name

class ChairImages(models.Model):
    color = models.ForeignKey(ChairColors, on_delete=models.CASCADE, related_name='chair_images')
    image = models.ImageField(upload_to='chair_images/')
    
    def __str__(self):
        return self.color.color_name

