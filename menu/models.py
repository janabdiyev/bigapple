from django.db import models


GROUP_CHOICES = [
    ("food", "Yiyecek"),
    ("drinks", "İçecek"),
    ("other", "Diğer"),
]


class Category(models.Model):
    """Top-level menu category (e.g. Burgerler, Biralar, Şaraplar)."""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    group = models.CharField(
        max_length=10,
        choices=GROUP_CHOICES,
        default="food",
        verbose_name="Grup",
        help_text="Yiyecek mi, içecek mi?",
    )
    # Self-referential: wine subcategories live under 'Şaraplar' parent
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subcategories",
        verbose_name="Üst Kategori",
        help_text="Bu kategori başka bir kategorinin alt kategorisiyse seçin.",
    )
    icon = models.CharField(
        max_length=10, blank=True, default="",
        verbose_name="İkon (emoji)",
        help_text="Opsiyonel emoji, örn: 🍔",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """A single menu item belonging to a category."""
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items", verbose_name="Kategori"
    )
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Fiyat (TL)"
    )
    image = models.ImageField(
        upload_to="menu_items/", blank=True, null=True, verbose_name="Resim"
    )
    order = models.IntegerField(default=0, verbose_name="Sıra")

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Menü Ürünü"
        verbose_name_plural = "Menü Ürünleri"

    def __str__(self):
        return self.name


class ItemSize(models.Model):
    """Size/portion variants for a menu item (e.g. 5cl / 8cl for spirits)."""
    item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="sizes", verbose_name="Ürün"
    )
    qty = models.CharField(max_length=50, verbose_name="Miktar / Boy")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat (TL)")
    order = models.IntegerField(default=0, verbose_name="Sıra")

    class Meta:
        ordering = ["order"]
        verbose_name = "Boy / Fiyat"
        verbose_name_plural = "Boy / Fiyatlar"

    def __str__(self):
        return f"{self.item.name} — {self.qty}"


# ──────────────────────────────────────────────
#  CAMPAIGN MENU (shown 12:30–16:30)
# ──────────────────────────────────────────────

class CampaignItem(models.Model):
    """Scrollable campaign banners shown during happy hour window."""
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    image = models.ImageField(
        upload_to="campaigns/", blank=True, null=True, verbose_name="Resim"
    )
    active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.IntegerField(default=0, verbose_name="Sıra")

    class Meta:
        ordering = ["order"]
        verbose_name = "Kampanya Menüsü"
        verbose_name_plural = "Kampanya Menüleri"

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
#  SITE SETTINGS (singleton)
# ──────────────────────────────────────────────

class SiteSettings(models.Model):
    """Global site settings — only ONE record should exist."""
    campaign_enabled = models.BooleanField(
        default=True,
        verbose_name="Kampanya Aktif",
        help_text="Kampanya menüsü zaman diliminde gösterilsin mi?",
    )
    campaign_start = models.TimeField(
        default="12:30",
        verbose_name="Kampanya Başlangıç Saati",
        help_text="Örn: 12:30",
    )
    campaign_end = models.TimeField(
        default="16:30",
        verbose_name="Kampanya Bitiş Saati",
        help_text="Örn: 16:30",
    )
    site_title = models.CharField(
        max_length=100, default="BIG APPLE PUB", verbose_name="Site Başlığı"
    )
    tagline = models.CharField(
        max_length=200,
        default="Taze, bol ve sipariş üzerine!",
        verbose_name="Alt Başlık",
    )

    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"

    def __str__(self):
        return "Site Ayarları"

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Sadece bir ayar kaydı olabilir.")
        super().save(*args, **kwargs)


# ──────────────────────────────────────────────
#  LANDING VIDEO (scroll-scrub animation)
# ──────────────────────────────────────────────

class LandingVideo(models.Model):
    """Video file used for the scroll-animated landing page."""
    video = models.FileField(
        upload_to="landing/",
        verbose_name="Video Dosyası",
        help_text="Mobil formatında video (MP4 önerilir). Scroll animasyonunda kullanılır.",
    )
    active = models.BooleanField(default=True, verbose_name="Aktif")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Landing Video"
        verbose_name_plural = "Landing Videolar"

    def __str__(self):
        return f"Landing Video — {'Aktif' if self.active else 'Pasif'} ({self.uploaded_at.strftime('%d.%m.%Y') if self.uploaded_at else ''})"


# ──────────────────────────────────────────────
#  PROMO POPUP (kept from old site)
# ──────────────────────────────────────────────

class PromoSettings(models.Model):
    enabled = models.BooleanField(
        default=True,
        verbose_name="Promosyon Popup Aktif",
    )

    class Meta:
        verbose_name = "Promosyon Ayarları"
        verbose_name_plural = "Promosyon Ayarları"

    def __str__(self):
        return f"Promosyon ({'Aktif' if self.enabled else 'Pasif'})"

    def save(self, *args, **kwargs):
        if not self.pk and PromoSettings.objects.exists():
            raise ValueError("Sadece bir promosyon ayarı olabilir.")
        super().save(*args, **kwargs)


class PromoImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    image = models.ImageField(upload_to="promo_images/", verbose_name="Resim")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    active = models.BooleanField(default=True, verbose_name="Aktif")
    link_to_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Bağlantılı Kategori",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Promosyon Resmi"
        verbose_name_plural = "Promosyon Resimleri"

    def __str__(self):
        return self.title
