# menu/models.py
from django.db import models


class Category(models.Model):
    """Existing Category model - don't modify"""
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Existing MenuItem model - don't modify"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class ItemSize(models.Model):
    """Existing ItemSize model - don't modify"""
    item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name='sizes')
    qty = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.item.name} - {self.qty}"


# ============= NEW PROMO FEATURE MODELS =============

class PromoSettings(models.Model):
    """Global settings for promo popup"""
    enabled = models.BooleanField(
        default=True,
        verbose_name="Promosyonları Aktif Et",
        help_text="Açılış promosyon resmlerini göster/gizle"
    )

    class Meta:
        verbose_name = "Promosyon Ayarları"
        verbose_name_plural = "Promosyon Ayarları"

    def __str__(self):
        return f"Promosyon Ayarları ({'Aktif' if self.enabled else 'Pasif'})"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and PromoSettings.objects.exists():
            raise ValueError(
                "PromoSettings instance already exists. Edit the existing one.")
        return super().save(*args, **kwargs)


class PromoImage(models.Model):
    """Promotional images shown on page load"""
    title = models.CharField(
        max_length=200,
        verbose_name="Başlık",
        help_text="Promosyon resmi için başlık"
    )
    image = models.ImageField(
        upload_to='promo_images/',
        verbose_name="Resim",
        help_text="Promosyon resmi (önerilen: 800x1000px veya benzer oran)"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Sıra",
        help_text="Gösterim sırası (küçükten büyüğe)"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Aktif",
        help_text="Bu resmi göster/gizle"
    )
    link_to_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Bağlantılı Kategori",
        help_text="Bu promosyon için menüde kategori seçin (opsiyonel)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Promosyon Resmi"
        verbose_name_plural = "Promosyon Resimleri"

    def __str__(self):
        return f"{self.title} ({'Aktif' if self.active else 'Pasif'})"
