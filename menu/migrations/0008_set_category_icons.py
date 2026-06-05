"""Sets emoji icons on existing categories based on name matching."""
from django.db import migrations


ICON_MAP = {
    'HAPPY HOURS':          '😁',
    'BURGERS':              '🍔',
    'SOSİSLİ':              '🌭',
    'KIZARTMA':             '🍟',
    'MAIN MENU':            '🍽️',
    'FISH MENU':            '🐟',
    'STARTERS':             '🥗',
    'KAHVALTI':             '🥚',
    'BİRALAR':              '🍺',
    'BIRALAR':              '🍺',
    'COCKTAILS':            '🍹',
    'ŞARAPLAR':             '🍷',
    'ŞİŞELER':              '🍾',
    'VİSKİLER':             '🥃',
    'CİNLER':               '🌿',
    'LİKORLER':             '🍬',
    'ROMLAR':               '🏝️',
    'SHOTLAR':              '🥃',
    'VOTKALAR':             '🧊',
    'APERATİF':             '🍊',
    'MEŞRUBAT':             '🥤',
    'KIRMIZI ŞARAP':        '🔴',
    'ROSE ŞARAP':           '🌸',
    'BEYAZ ŞARAP':          '🤍',
    'YARI TATLI':           '🍯',
    'ANA YEMEKLER':         '🍽️',
    'BALIK':                '🐟',
    'BAŞLANGIÇ':            '🥗',
    'SALATA':               '🥗',
}


def set_icons(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    for cat in Category.objects.all():
        if cat.icon:
            continue  # already has icon, skip
        name_upper = cat.name.upper()
        for keyword, icon in ICON_MAP.items():
            if keyword in name_upper:
                cat.icon = icon
                cat.save(update_fields=['icon'])
                break


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_category_order'),
    ]

    operations = [
        migrations.RunPython(set_icons, noop),
    ]
