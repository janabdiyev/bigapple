"""
Data migration: assigns group (food/drinks) and parent (wine subcats)
to existing categories, and creates default SiteSettings.
Runs automatically on deploy — never deletes or modifies existing data.
"""
from django.db import migrations


FOOD_KEYWORDS = [
    'HAPPY HOURS', 'BURGERS', 'SOSİSLİ', 'KIZARTMA',
    'MAIN MENU', 'FISH MENU', 'STARTERS', 'BAŞLANGIÇ',
    'ANA YEMEKLER', 'BALIK', 'KAHVALTI', 'SALATA',
]

DRINKS_KEYWORDS = [
    'BİRALAR', 'BIRALAR', 'COCKTAILS', 'ŞARAPLAR', 'SARAPLAR',
    'KIRMIZI ŞARAP', 'ROSE ŞARAP', 'BEYAZ ŞARAP', 'YARI TATLI',
    'ŞİŞELER', 'VİSKİLER', 'CİNLER', 'LİKORLER', 'ROMLAR',
    'SHOTLAR', 'VOTKALAR', 'APERATİF', 'MEŞRUBAT', 'ALKOLSÜZ',
]

WINE_SUBCAT_KEYWORDS = [
    'KIRMIZI ŞARAP', 'ROSE ŞARAP', 'BEYAZ ŞARAP', 'YARI TATLI',
    'KIRMIZI SARAP', 'ROSE SARAP', 'BEYAZ SARAP',
]


def assign_groups(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    SiteSettings = apps.get_model('menu', 'SiteSettings')

    # Find wine parent
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

        for keyword in FOOD_KEYWORDS:
            if keyword in name_upper:
                group = 'food'
                break

        if group == 'other':
            for keyword in DRINKS_KEYWORDS:
                if keyword in name_upper:
                    group = 'drinks'
                    break

        parent = None
        if wine_parent and any(kw in name_upper for kw in WINE_SUBCAT_KEYWORDS):
            parent = wine_parent
            group = 'drinks'

        update_fields = []
        if cat.group != group:
            cat.group = group
            update_fields.append('group')
        if parent and cat.parent_id != parent.pk:
            cat.parent = parent
            update_fields.append('parent')
        if update_fields:
            cat.save(update_fields=update_fields)

    # Create default SiteSettings if not exists
    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(
            site_title='BIG APPLE PUB',
            tagline='Taze, bol ve sipariş üzerine!',
            campaign_enabled=True,
            campaign_start='12:30',
            campaign_end='16:30',
        )


def reverse_assign(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    Category.objects.all().update(group='food', parent=None)


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_add_new_models'),
    ]

    operations = [
        migrations.RunPython(assign_groups, reverse_assign),
    ]
