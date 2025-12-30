# menu/views.py
from django.shortcuts import render
from .models import Category, PromoImage, PromoSettings


def menu_view(request):
    """Display menu with optional promo popup"""
    categories = Category.objects.prefetch_related('menuitem_set__sizes').all()

    # Get promo settings
    try:
        promo_settings = PromoSettings.objects.first()
        promo_enabled = promo_settings.enabled if promo_settings else False
    except:
        promo_enabled = False

    # Get active promo images if enabled
    promo_images = []
    if promo_enabled:
        promo_images = PromoImage.objects.filter(
            active=True).order_by('order', 'created_at')

    context = {
        'categories': categories,
        'promo_enabled': promo_enabled,
        'promo_images': promo_images,
    }

    return render(request, 'menu/menu.html', context)
