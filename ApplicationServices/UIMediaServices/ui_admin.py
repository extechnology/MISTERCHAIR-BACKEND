from django.contrib import admin
from django.utils.html import mark_safe

from .ui_models import (
    LandingImage,
    ShopByCategory,
)


@admin.register(LandingImage)
class LandingImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'landscape_image_preview', 'portrait_image_preview')
    ordering = ('title',)

    def landscape_image_preview(self, obj):
        if obj.image_landscap:
            return mark_safe(
                f'<img src="{obj.image_landscap.url}" width="240" height="116" style="object-fit:cover;border-radius:6px;" />'
            )
        return "No Image"

    landscape_image_preview.short_description = "Landscape Image Preview"

    def portrait_image_preview(self, obj):
        if obj.image_portrait:
            return mark_safe(
                f'<img src="{obj.image_portrait.url}" width="240" height="116" style="object-fit:cover;border-radius:6px;" />'
            )
        return "No Image"

    portrait_image_preview.short_description = "Portrait Image Preview"


@admin.register(ShopByCategory)
class ShopByCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
