from django.db import models
from ApplicationServices.ProductServices.product_models import (
    Category,
)
class LandingImage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_landscap = models.ImageField(upload_to='landing_images/landscape/',help_text="Image for Desktop")
    image_portrait = models.ImageField(upload_to='landing_images/portrait/',help_text="Image for Mobile")

    def __str__(self):
        return self.title


class ShopByCategory(models.Model):
    categories = models.ManyToManyField(Category,related_name="shop_by_category",help_text="Maximum 5 categories")

    def __str__(self):
        return "Shop By Category"

        