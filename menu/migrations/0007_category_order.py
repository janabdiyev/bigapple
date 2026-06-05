"""
Adds `order` to Category safely — skips if column already exists
(handles the case where it was added manually to the live DB).
"""
from django.db import migrations, connection


def add_order_column(apps, schema_editor):
    # Check if column already exists before adding
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(menu_category)")
        columns = [row[1] for row in cursor.fetchall()]
    if 'order' not in columns:
        with connection.cursor() as cursor:
            cursor.execute(
                'ALTER TABLE menu_category ADD COLUMN "order" integer NOT NULL DEFAULT 0'
            )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_assign_groups'),
    ]

    operations = [
        migrations.RunPython(add_order_column, noop),
    ]
