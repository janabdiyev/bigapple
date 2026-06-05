from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, MenuItem, ItemSize,
    CampaignItem, SiteSettings, LandingVideo,
    PromoSettings, PromoImage,
)

admin.site.site_header = "Big Apple Pub — Dashboard"
admin.site.site_title = "Big Apple Admin"
admin.site.index_title = "Yönetim Paneli"


# ── Inlines ───────────────────────────────────────────────────

class ItemSizeInline(admin.TabularInline):
    model = ItemSize
    extra = 1
    fields = ["qty", "price", "order"]


class SubCategoryInline(admin.TabularInline):
    model = Category
    fk_name = "parent"
    extra = 0
    fields = ["name", "icon", "order"]
    show_change_link = True
    verbose_name = "Alt Kategori"
    verbose_name_plural = "Alt Kategoriler"


# ── Category ──────────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "parent", "icon", "order"]
    list_editable = ["order", "group", "icon"]
    list_filter = ["group", "parent"]
    ordering = ["group", "order", "name"]
    inlines = [SubCategoryInline]
    fieldsets = (
        (None, {"fields": ("name", "icon", "group", "parent", "order")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("parent")


# ── MenuItem ──────────────────────────────────────────────────

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "image_preview", "order"]
    list_filter = ["category__group", "category"]
    list_editable = ["order"]
    search_fields = ["name", "description"]
    inlines = [ItemSizeInline]
    ordering = ["category__group", "category__order", "order", "name"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:48px;border-radius:6px;" />', obj.image.url
            )
        return "—"
    image_preview.short_description = "Resim"


# ── Campaign ──────────────────────────────────────────────────

@admin.register(CampaignItem)
class CampaignItemAdmin(admin.ModelAdmin):
    list_display = ["title", "active", "order", "image_preview"]
    list_editable = ["active", "order"]
    ordering = ["order"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px;border-radius:6px;" />', obj.image.url
            )
        return "—"
    image_preview.short_description = "Resim"


# ── Site Settings ─────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Genel", {"fields": ("site_title", "tagline")}),
        ("Kampanya Zamanlaması", {
            "fields": ("campaign_enabled", "campaign_start", "campaign_end"),
            "description": "Kampanya menüsü yalnızca bu zaman diliminde yiyecek sayfasında gösterilir.",
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Landing Video ─────────────────────────────────────────────

@admin.register(LandingVideo)
class LandingVideoAdmin(admin.ModelAdmin):
    list_display = ["__str__", "active", "uploaded_at", "video_preview"]
    list_editable = ["active"]
    ordering = ["-uploaded_at"]

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video src="{}" style="max-height:60px;" controls muted></video>', obj.video.url
            )
        return "—"
    video_preview.short_description = "Önizleme"


# ── Promo ─────────────────────────────────────────────────────

@admin.register(PromoSettings)
class PromoSettingsAdmin(admin.ModelAdmin):
    list_display = ["__str__", "enabled"]

    def has_add_permission(self, request):
        return not PromoSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PromoImage)
class PromoImageAdmin(admin.ModelAdmin):
    list_display = ["title", "active", "order", "image_preview", "created_at"]
    list_editable = ["active", "order"]
    ordering = ["order", "created_at"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:50px;border-radius:6px;" />', obj.image.url
            )
        return "—"
    image_preview.short_description = "Önizleme"
