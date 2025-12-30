# Generated migration file for promo feature
# Save as: menu/migrations/0002_promo_feature.py

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_menuitem_price'),  # ✅ Correct
    ]

    operations = [
        migrations.CreateModel(
            name='PromoSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(
                    default=True, help_text='Açılış promosyon resmlerini göster/gizle', verbose_name='Promosyonları Aktif Et')),
            ],
            options={
                'verbose_name': 'Promosyon Ayarları',
                'verbose_name_plural': 'Promosyon Ayarları',
            },
        ),
        migrations.CreateModel(
            name='PromoImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(
                    help_text='Promosyon resmi için başlık', max_length=200, verbose_name='Başlık')),
                ('image', models.ImageField(help_text='Promosyon resmi (önerilen: 800x1000px veya benzer oran)',
                 upload_to='promo_images/', verbose_name='Resim')),
                ('order', models.IntegerField(
                    default=0, help_text='Gösterim sırası (küçükten büyüğe)', verbose_name='Sıra')),
                ('active', models.BooleanField(default=True,
                 help_text='Bu resmi göster/gizle', verbose_name='Aktif')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('link_to_category', models.ForeignKey(blank=True, help_text='Bu promosyon için menüde kategori seçin (opsiyonel)',
                 null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.category', verbose_name='Bağlantılı Kategori')),
            ],
            options={
                'verbose_name': 'Promosyon Resmi',
                'verbose_name_plural': 'Promosyon Resimleri',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]
