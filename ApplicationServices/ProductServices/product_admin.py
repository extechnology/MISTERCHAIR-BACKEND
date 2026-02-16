from django.contrib import admin
from django.utils.html import format_html
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


class ChairColorsInline(NestedStackedInline):
    model = ChairColors
    extra = 1
    max_num = 10
    inlines = [ChairImagesInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)


@admin.register(Chair)
class ChairAdmin(NestedModelAdmin):
    list_display = ('name', 'category', 'minimum_order_quantity')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [ChairColorsInline]


@admin.register(ChairColors)
class ChairColorsAdmin(admin.ModelAdmin):
    list_display = ('chair', 'color_name', 'color_code', 'color_code_2', 'price', 'discount_price', 'if_discount', 'is_available', 'available_stock')
    list_filter = ('chair', 'if_discount', 'is_available')
    search_fields = ('chair__name', 'color_name', 'color_code', 'color_code_2')
    ordering = ('chair', 'color_name')


@admin.register(ChairImages)
class ChairImagesAdmin(admin.ModelAdmin):
    list_display = ('get_chair', 'color', 'image')
    list_filter = ('color__chair', 'color')
    search_fields = ('color__chair__name', 'color__color_name')
    ordering = ('color',)

    @admin.display(description='Chair', ordering='color__chair')
    def get_chair(self, obj):
        return obj.color.chair