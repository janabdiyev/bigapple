# menu/models.py
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    menu_item = models.ForeignKey(
        'MenuItem', on_delete=models.CASCADE, related_name='sizes')
    qty = models.CharField(max_length=20, blank=True,
                           help_text="For Example: 4 cl, 33 cl, 1 lt")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.qty} – {self.price} TL"


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    # ADD THIS LINE
    price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)

    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    # REMOVE DUPLICATE image_thumbnail and __str__
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 80}
    )

    def __str__(self):
        return f"{self.name} ({self.category.name})"
