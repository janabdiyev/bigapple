"""
Data migration: assigns group (food/drinks) and parent (wine subcats)
to existing Category records, and creates a default SiteSettings.

Runs automatically on `python manage.py migrate`.
Safe to run on the live Render DB — only adds data to new fields,
never deletes or modifies existing items/prices/images.
"""
from django.db import migrations


# Map every known category name → group
# Keys are matched case-insensitively and with startswith/contains logic
FOOD_NAMES = {
    'HAPPY HOURS',
    'BURGERS',
    'SOSİSLİ',
    'KIZARTMA',
    'MAIN MENU',
    'FISH MENU',
    'STARTERS',
    'ANA YEMEKLER',
    'BALIK',
    'BAŞLANGIÇ',
    'KAHVALTI',
    'SALATA',
}

DRINKS_NAMES = {
    'BİRALAR',
    'BIRALAR',
    'COCKTAILS',
    'KOKTEYLLERİ',
    'ŞARAPLAR',
    'SARAPLAR',
    'KIRMIZI ŞARAP',
    'ROSE ŞARAP',
    'BEYAZ ŞARAP',
    'YARI TATLI',
    'ŞİŞELER',
    'VİSKİLER',
    'CİNLER',
    'LİKORLER',
    'ROMLAR',
    'SHOTLAR',
    'VOTKALAR',
    'APERATİF',
    'MEŞRUBAT',
    'ALKOLSÜZ',
}

WINE_SUBCAT_KEYWORDS = [
    'KIRMIZI ŞARAP',
    'ROSE ŞARAP',
    'BEYAZ ŞARAP',
    'YARI TATLI',
    'KIRMIZI SARAP',
    'ROSE SARAP',
    'BEYAZ SARAP',
]


def assign_groups(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    SiteSettings = apps.get_model('menu', 'SiteSettings')

    # Find the wine parent category
    wine_parent = None
    for cat in Category.objects.all():
        name_upper = cat.name.upper()
        if ('ŞARAP' in name_upper or 'SARAP' in name_upper) and \
           not any(kw in name_upper for kw in ['KIRMIZI', 'ROSE', 'BEYAZ', 'YARI']):
            wine_parent = cat
            break

    for cat in Category.objects.all():
        name_upper = cat.name.upper()
        group = 'other'

        # Check food
        for keyword in FOOD_NAMES:
            if keyword in name_upper:
                group = 'food'
                break

        # Check drinks
        if group == 'other':
            for keyword in DRINKS_NAMES:
                if keyword in name_upper:
                    group = 'drinks'
                    break

        # Assign parent for wine subcats
        parent = None
        if wine_parent and any(kw in name_upper for kw in
                               ['KIRMIZI ŞARAP', 'ROSE ŞARAP', 'BEYAZ ŞARAP', 'YARI TATLI',
                                'KIRMIZI SARAP', 'ROSE SARAP', 'BEYAZ SARAP']):
            parent = wine_parent
            group = 'drinks'

        # Only update if something changed
        update_fields = []
        if cat.group != group:
            cat.group = group
            update_fields.append('group')
        if parent and cat.parent_id != parent.pk:
            cat.parent = parent
            update_fields.append('parent')

        if update_fields:
            cat.save(update_fields=update_fields)

    # Create default SiteSettings if none exists
    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(
            site_title='BIG APPLE PUB',
            tagline='Taze, bol ve sipariş üzerine!',
            campaign_enabled=True,
            campaign_start='12:30',
            campaign_end='16:30',
        )


def reverse_assign_groups(apps, schema_editor):
    # Reversible: just set everything back to 'food' (default)
    Category = apps.get_model('menu', 'Category')
    Category.objects.all().update(group='food', parent=None)


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(assign_groups, reverse_assign_groups),
    ]
