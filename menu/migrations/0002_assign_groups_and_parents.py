# This migration is intentionally a no-op pass-through.
# It exists to bridge the old migration history (0001-0004) with
# the new migrations (0005+). All actual work is in 0005 and 0006.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_promo_feature'),
    ]

    operations = []
