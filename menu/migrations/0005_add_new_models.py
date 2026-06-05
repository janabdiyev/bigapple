"""
Adds new fields and models on top of the existing live DB.
Safe — never touches existing data, only adds columns and tables.
"""
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_assign_groups_and_parents'),
    ]

    operations = [
        # ── Category: add group, parent, icon ─────────────────
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.CharField(
                choices=[('food', 'Yiyecek'), ('drinks', 'İçecek'), ('other', 'Diğer')],
                default='food',
                max_length=10,
                verbose_name='Grup',
            ),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='subcategories',
                to='menu.category',
                verbose_name='Üst Kategori',
            ),
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='İkon (emoji)'),
        ),

        # ── MenuItem: add related_name='items' (DB no-op) ─────
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='items',
                to='menu.category',
                verbose_name='Kategori',
            ),
        ),

        # ── CampaignItem ──────────────────────────────────────
        migrations.CreateModel(
            name='CampaignItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Başlık')),
                ('description', models.TextField(blank=True, verbose_name='Açıklama')),
                ('image', models.ImageField(blank=True, null=True, upload_to='campaigns/', verbose_name='Resim')),
                ('active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('order', models.IntegerField(default=0, verbose_name='Sıra')),
            ],
            options={
                'verbose_name': 'Kampanya Menüsü',
                'verbose_name_plural': 'Kampanya Menüleri',
                'ordering': ['order'],
            },
        ),

        # ── SiteSettings ──────────────────────────────────────
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_enabled', models.BooleanField(default=True, verbose_name='Kampanya Aktif')),
                ('campaign_start', models.TimeField(default='12:30', verbose_name='Kampanya Başlangıç Saati')),
                ('campaign_end', models.TimeField(default='16:30', verbose_name='Kampanya Bitiş Saati')),
                ('site_title', models.CharField(default='BIG APPLE PUB', max_length=100, verbose_name='Site Başlığı')),
                ('tagline', models.CharField(default='Taze, bol ve sipariş üzerine!', max_length=200, verbose_name='Alt Başlık')),
            ],
            options={
                'verbose_name': 'Site Ayarları',
                'verbose_name_plural': 'Site Ayarları',
            },
        ),

        # ── LandingVideo ─────────────────────────────────────
        migrations.CreateModel(
            name='LandingVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='landing/', verbose_name='Video Dosyası')),
                ('active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Landing Video',
                'verbose_name_plural': 'Landing Videolar',
            },
        ),
    ]
