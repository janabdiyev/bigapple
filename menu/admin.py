# menu/admin.py
from django.contrib import admin
from .models import Category, MenuItem, Size


class SizeInline(admin.TabularInline):
    model = Size
    extra = 1
    fields = ('qty', 'price')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['category']
    readonly_fields = ['image_thumbnail_preview']
    inlines = [SizeInline]

    def image_thumbnail_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image_thumbnail.url}" style="width:80px;height:80px;object-fit:cover;border-radius:8px;">'
        return "(No image)"
    image_thumbnail_preview.short_description = "Preview"
    image_thumbnail_preview.allow_tags = True
