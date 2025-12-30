# menu/admin.py
from django.contrib import admin
from .models import Category, MenuItem, ItemSize, PromoImage, PromoSettings

# ============= EXISTING ADMIN REGISTRATIONS =============


class ItemSizeInline(admin.TabularInline):
    model = ItemSize
    extra = 1
    fields = ['qty', 'price', 'order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    ordering = ['order', 'name']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'order']
    list_filter = ['category']
    list_editable = ['order']
    search_fields = ['name', 'description']
    inlines = [ItemSizeInline]
    ordering = ['category', 'order', 'name']


# ============= NEW PROMO FEATURE ADMIN =============

@admin.register(PromoSettings)
class PromoSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'enabled']

    def has_add_permission(self, request):
        # Only allow one instance
        return not PromoSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(PromoImage)
class PromoImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'order',
                    'link_to_category', 'image_preview', 'created_at']
    list_editable = ['active', 'order']
    list_filter = ['active', 'link_to_category']
    search_fields = ['title']
    ordering = ['order', 'created_at']

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'image', 'order', 'active')
        }),
        ('Kategori Bağlantısı (Opsiyonel)', {
            'fields': ('link_to_category',),
            'description': 'Promosyonda gösterilen ürünler için menüde bir kategori seçebilirsiniz.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height:50px; max-width:100px; object-fit:cover;" />'
        return "Resim yok"
    image_preview.short_description = "Önizleme"
    image_preview.allow_tags = True
