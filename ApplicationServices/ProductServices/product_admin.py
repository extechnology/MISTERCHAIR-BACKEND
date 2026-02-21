from django.contrib import admin
from django.utils.html import mark_safe
from nested_admin import (
    NestedModelAdmin, 
    NestedTabularInline, 
    NestedStackedInline
    )

from .product_models import (
    Category,
    Chair,
    ChairColors,
    ChairImages,
    )

class ChairImagesInline(NestedTabularInline):
    model = ChairImages
    extra = 1
    max_num = 10
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="120" height="120" style="object-fit:cover;border-radius:6px;" />'
            )
        return "No Image"

    image_preview.short_description = "Preview"



class ChairColorsInline(NestedStackedInline):
    model = ChairColors
    extra = 1
    max_num = 10
    inlines = [ChairImagesInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_image_preview')
    list_filter = ('category_name',)
    search_fields = ('category_name',)
    ordering = ('category_name',)
    list_per_page = 5
    list_max_show_all = 1000

    def category_image_preview(self, obj):
        if obj.category_image:
            return mark_safe(
                f'<img src="{obj.category_image.url}" width="150" height="100" style="object-fit:cover;border-radius:6px;" />'
            )
        return "No Image"

    category_image_preview.short_description = "Preview"


@admin.register(Chair)
class ChairAdmin(NestedModelAdmin):
    list_display = ('name', 'category', 'minimum_order_quantity', 'image_preview','price','special_tag')
    list_filter = ('category', 'minimum_order_quantity','special_tag')
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [ChairColorsInline]
    readonly_fields = ('image_preview','price')

    list_per_page = 5          # items per page
    list_max_show_all = 200     # max items when clicking "Show all"

    def image_preview(self, obj):
        # get first image through relations
        image = (
            obj.chair_colors
            .prefetch_related('chair_images')
            .values_list('chair_images__image', flat=True)
            .first()
        )

        if image:
            return mark_safe(
                f'<img src="/media/{image}" width="240" height="116" '
                f'style="object-fit:cover;border-radius:6px;" />'
            )
        return "No Image"

    image_preview.short_description = "Preview"

    def price(self, obj):
        return obj.chair_colors.first().price

    price.short_description = "Price"

@admin.register(ChairColors)
class ChairColorsAdmin(admin.ModelAdmin):
    list_display = (
        'chair', 'color_name', 'color_preview',
        'color_code', 'color_code_2',
        'price', 'discount_price', 'if_discount',
        'is_available', 'available_stock'
    )
    list_filter = ('chair', 'if_discount', 'is_available')
    search_fields = ('chair__name', 'color_name', 'color_code', 'color_code_2')
    ordering = ('chair', 'color_name')

    list_per_page = 5
    list_max_show_all = 10000

    def color_preview(self, obj):
        # If both colors exist → gradient
        if obj.color_code and obj.color_code_2:
            style = (
                f"background: linear-gradient(90deg, "
                f"{obj.color_code}, {obj.color_code_2});"
            )
        # Only one color → solid
        elif obj.color_code:
            style = f"background-color: {obj.color_code};"
        else:
            style = "background-color: #ffffff;"

        return mark_safe(
            f"""
            <div style="
                width:120px;
                height:40px;
                border:1px solid #000;
                border-radius:4px;
                {style}
            "></div>
            """
        )

    color_preview.short_description = "Color Preview"


@admin.register(ChairImages)
class ChairImagesAdmin(admin.ModelAdmin):
    list_display = ('get_chair', 'color', 'image_preview')
    readonly_fields = ('image_preview',)
    list_filter = ('color__chair', 'color')
    search_fields = ('color__chair__name', 'color__color_name')
    ordering = ('color',)

    list_per_page = 5          # items per page
    list_max_show_all = 10000     # max items when clicking "Show all"

    @admin.display(description='Chair', ordering='color__chair')
    def get_chair(self, obj):
        return obj.color.chair

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="240" height="116" style="object-fit:cover;border-radius:6px;" />'
            )
        return "No Image"

    image_preview.short_description = "Preview"
