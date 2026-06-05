from django.shortcuts import render
from django.utils import timezone
from .models import Category, CampaignItem, SiteSettings, LandingVideo, PromoImage, PromoSettings
import json


def menu_view(request):
    settings = SiteSettings.objects.first()

    # ── Campaign visibility check ──────────────────────────────
    show_campaigns = False
    campaigns = []
    if settings and settings.campaign_enabled:
        now = timezone.localtime().time()
        if settings.campaign_start <= now <= settings.campaign_end:
            show_campaigns = True
            campaigns = list(
                CampaignItem.objects.filter(active=True).order_by("order").values(
                    "id", "title", "description", "image"
                )
            )
            # Build full image URLs
            for c in campaigns:
                if c["image"]:
                    c["image_url"] = f"/media/{c['image']}"
                else:
                    c["image_url"] = None

    # ── Landing video ──────────────────────────────────────────
    landing_video = LandingVideo.objects.filter(active=True).order_by("-uploaded_at").first()

    # ── Categories (food + drinks) ─────────────────────────────
    # Only top-level categories (parent=None)
    top_categories = Category.objects.filter(parent=None).prefetch_related(
        "subcategories__items__sizes",
        "items__sizes",
    ).order_by("order", "name")

    food_cats = [c for c in top_categories if c.group == "food"]
    drinks_cats = [c for c in top_categories if c.group == "drinks"]

    def serialize_item(item):
        sizes = [{"qty": s.qty, "price": str(s.price)} for s in item.sizes.all()]
        return {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": str(item.price) if item.price else None,
            "image_url": item.image.url if item.image else None,
            "sizes": sizes,
        }

    def serialize_category(cat):
        subs = []
        for sub in cat.subcategories.order_by("order", "name"):
            subs.append({
                "id": sub.id,
                "name": sub.name,
                "icon": sub.icon,
                "items": [serialize_item(i) for i in sub.items.all()],
            })
        return {
            "id": cat.id,
            "name": cat.name,
            "icon": cat.icon,
            "subcategories": subs,
            "items": [serialize_item(i) for i in cat.items.all()] if not subs else [],
        }

    food_data = [serialize_category(c) for c in food_cats]
    drinks_data = [serialize_category(c) for c in drinks_cats]

    # ── Promo popup ────────────────────────────────────────────
    try:
        promo_settings = PromoSettings.objects.first()
        promo_enabled = promo_settings.enabled if promo_settings else False
    except Exception:
        promo_enabled = False

    promo_images = []
    if promo_enabled:
        promo_images = [
            {"url": img.image.url, "title": img.title}
            for img in PromoImage.objects.filter(active=True).order_by("order", "created_at")
        ]

    context = {
        "settings": settings,
        "landing_video": landing_video,
        "show_campaigns": show_campaigns,
        "campaigns_json": json.dumps(campaigns, ensure_ascii=False),
        "food_json": json.dumps(food_data, ensure_ascii=False),
        "drinks_json": json.dumps(drinks_data, ensure_ascii=False),
        "promo_enabled": promo_enabled,
        "promo_images_json": json.dumps(promo_images, ensure_ascii=False),
    }

    return render(request, "menu/menu.html", context)
