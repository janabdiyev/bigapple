# Big Apple Pub — Project Memory

Last updated: 2026-06-04

---

## Project Overview

**Site:** bigapple.pub (live on Render.com)
**GitHub:** https://github.com/janabdiyev/bigapple
**Owner:** Can Abdiyev — canabdiyev@gmail.com
**Type:** Mobile pub menu website — customers scan/open on their phones at the table

---

## Infrastructure

| Component | Detail |
|-----------|--------|
| Hosting | Render.com (web service) |
| Database | SQLite at `/var/data/db.sqlite3` (Render persistent disk) |
| Media files | `/var/data/media/` (Render persistent disk) |
| Static files | WhiteNoise via Django |
| Deploy trigger | Push to GitHub `main` → Render auto-deploys |
| Python | 3.12 (Anaconda on local Mac) |
| Django | 4.2.x |

**Critical:** All live data (prices, images, descriptions) lives on the Render persistent disk — NOT in the GitHub repo. Never wipe the persistent disk.

---

## Local Project Structure

**Working folder:** `/Users/kakajanabdiyev/Desktop/newapple_project/new big apple page/`  
**Old site reference:** `/Users/kakajanabdiyev/Desktop/newapple_project/oldsite/`

```
new big apple page/
├── bigapple/          # Django project config
├── menu/              # Main app
│   ├── migrations/    # 0001_initial, 0002_assign_groups_and_parents
│   ├── templates/menu/menu.html   # Full SPA template
│   ├── management/commands/load_menu.py  # Seeds local DB
│   ├── models.py      # All models
│   ├── views.py       # Single view, serves JSON to SPA
│   └── admin.py       # Dashboard
├── static/images/logo.png
├── media/menu_images/ # Images (also on Render persistent disk)
├── db.sqlite3         # Local only
├── requirements.txt
└── manage.py
```

**Local setup commands:**
```bash
cd "new big apple page"
pip install -r requirements.txt
python manage.py migrate
python manage.py load_menu    # seeds all 250+ items
python manage.py createsuperuser
python manage.py runserver
```

---

## Data Models

### Category
- `name`, `order`, `group` (food/drinks/other), `parent` (FK to self — wine subcats), `icon` (emoji)

### MenuItem
- FK to Category, `name`, `description`, `price`, `image`, `order`

### ItemSize
- FK to MenuItem — for spirits/wines with multiple pour sizes (e.g. 5cl/8cl)

### CampaignItem
- Campaign banners shown 12:30–16:30 — `title`, `description`, `image`, `active`, `order`

### SiteSettings (singleton)
- `site_title`, `tagline`, `campaign_enabled`, `campaign_start` (12:30), `campaign_end` (16:30)

### LandingVideo
- Video file for scroll animation on landing page — uploaded via admin dashboard

### PromoSettings + PromoImage
- Popup images shown on page load (kept from old site)

---

## Category Structure (live DB names — exact)

### Food
| Name | Notes |
|------|-------|
| 😁 HAPPY HOURS 😁 | Mon–Thu combo deals |
| 🍔 BURGERS | |
| SOSİSLİ | |
| KIZARTMA | |
| MAIN MENU | (not "Ana Yemekler") |
| FISH MENU | (not "Balık Menüsü") |
| STARTERS | (not "Başlangıçlar") |
| KAHVALTI | |

### Drinks
| Name | Notes |
|------|-------|
| 🍺 BİRALAR | (emoji is part of name) |
| 🍹 COCKTAILS | (emoji is part of name) |
| ŞARAPLAR | Parent category — has 4 wine subcats |
| ŞİŞELER | Bottle service |
| VİSKİLER | |
| CİNLER | |
| LİKORLER | |
| ROMLAR | |
| SHOTLAR | |
| VOTKALAR | |
| APERATİF | |
| MEŞRUBAT | Soft drinks |

### Wine subcategories (children of ŞARAPLAR)
- KIRMIZI ŞARAPLAR, ROSE ŞARAPLAR, BEYAZ ŞARAPLAR, YARI TATLI ŞARAPLAR

---

## Frontend Architecture (SPA)

Single HTML page — 4 screens shown/hidden by JavaScript:

1. **Landing** — scroll-animated (video scrub on scroll), reveals Food/Drinks buttons
2. **Food / Drinks** — category card grid (2 cols), campaign strip 12:30–16:30
3. **Category** — subcategory list (only for ŞARAPLAR), or goes straight to items
4. **Items** — full scrollable 2-per-row grid, tap card = bottom sheet modal

Navigation: bottom nav (Home/Food/Drinks) + back button in header

---

## Key Design Decisions

- **No pagination** — all items show at once, user scrolls (pub context = no pagination tolerance)
- **Dark luxury** — `#080808` black, `#c9a84c` gold, Playfair Display headings, Inter body
- **Mobile-first** — `100dvh`, `-webkit-tap-highlight-color: transparent`, safe-area insets
- **PWA-ready** — `apple-mobile-web-app-capable`, `theme-color: #080808`, black status bar
- **Item descriptions** — 12px, 3-line clamp on card; full text in modal
- **No max-scale** — pinch-to-zoom allowed (accessibility)

---

## Migrations

| File | Purpose |
|------|---------|
| `0001_initial` | Creates all new tables + columns |
| `0002_assign_groups_and_parents` | Data migration — auto-assigns food/drinks group to existing categories on Render deploy. Safe, never deletes data. |

**Render deploy flow:**
1. Push new code → Render auto-deploys
2. `migrate` runs → adds new columns, assigns groups
3. All live prices/items/images on persistent disk remain untouched
4. Admin: set `group` on any unrecognised categories manually if needed

---

## Known Live DB Quirks (preserved exactly as-is)

These are the exact names in the live DB — do NOT "fix" them:
- `TURBORG FİLTRESİZ` / `TURBORG ICE` (not Tuborg)
- `BOMONTİ FİLTESİZ` (missing R)
- `BUDWEISSER` (double S)
- `DISSARONNA` (not Disaronno)
- `CAPTAINMORGAN WHITE` (no space)
- `ABSOLUT EXTRAT` / `ABSOLUT VANLLA` (typos)
- `GORDONS SICILLIAN LEMONADE` (not Turkish)
- `GLENKINCHE 12` (not Glenkinchie)
- `COAL ILA 12` (not Caol Ila)
- `EFES MALT 50 CL`, `CARLSBERG 50 CL` etc. — size is part of the item name
- Wine sizes use `SİSE` not `ŞİŞE`
- `Red Bull Classic` / `Red Bull Sugarfree` — mixed case

**Deleted items:** `FETTUCINI ALFREDO` was deleted from live DB on 2026-06-03

---

## Missing Media Files

These images exist on the Render persistent disk but not locally.  
Download from browser: `https://www.bigapple.pub/media/menu_images/[filename]`  
Save to: `new big apple page/media/menu_images/`

- `IMG_4687.jpg` (BIG BOSS)
- `IMG_6618.JPG` (BIG APPLE BURGER)
- `IMG_8848.jpeg` (PREMIUM BURGER)
- `IMG_2525.jpg` (MINI BURGER)
- `IMG_6706.jpeg` (BIG ANTRİKOT)
- `WhatsApp_Image_2025-03-24_at_15.33.12.jpg` (IZGARA TAVUK BURGER)
- `Screenshot_2025-12-05_at_21.00.19.png` (WRAP 06)
- `Screenshot_2025-12-05_at_21.15.53.png` (TUBORG GOLD)
- `Screenshot_2025-12-05_at_12.45.15.png` (BIG LONG ISLAND)
- `Screenshot_2025-12-05_at_12.58.52.png` (CHALLENGER)
- `Screenshot_2025-12-05_at_12.43.18.png` (KIWI SMASH)
- `Screenshot_2025-12-05_at_13.00.55.png` (KUZU KULAĞI GIN)
- `Screenshot_2025-12-05_at_12.48.09.png` (LYNCHBURG LEMONADE)
- `Screenshot_2025-12-05_at_12.55.18.png` (MARGARİTA)
- `Screenshot_2025-12-05_at_12.53.55.png` (MOJİTO)
- `Screenshot_2025-12-05_at_12.50.19.png` (PORN STAR MARTİNİ)
- `Screenshot_2025-12-05_at_12.47.25.png` (WHISKEY SOUR)

---

## Go-Live Deployment Plan

### What to push to GitHub
Copy contents of `new big apple page/` into the local GitHub repo clone, replacing:
- `requirements.txt` — simpler (no imagekit/easy-thumbnails/django-imagekit)
- `bigapple/settings.py`, `bigapple/urls.py`
- `menu/models.py`, `menu/views.py`, `menu/admin.py`, `menu/urls.py`
- `menu/templates/menu/menu.html` — full SPA
- `menu/migrations/0001_initial.py`, `menu/migrations/0002_assign_groups_and_parents.py`
- `menu/management/__init__.py`, `menu/management/commands/__init__.py`
- `menu/management/commands/load_menu.py` — local dev only, not used on Render
- `.gitignore` — now excludes `media/` (Render has real images on persistent disk)
- `static/images/logo.png`

**Do NOT push:** `db.sqlite3`, `media/` folder (both gitignored)

### What Render does automatically on deploy
1. `pip install -r requirements.txt` — installs new simpler deps
2. `python manage.py migrate` — runs 0001 (new tables/columns) + 0002 (assigns food/drinks groups to existing categories)
3. Starts gunicorn — serves new site
4. **Persistent disk untouched** — `/var/data/db.sqlite3` and `/var/data/media/` stay intact

### After deploy — verify in admin
- Go to `/admin` → Kategoriler — confirm all categories have correct `group` (food/drinks)
- If any show `other`, manually set them in admin
- Check SiteSettings exists (migration creates it if missing)
- Upload landing video via admin → Landing Video section

### Critical: Old code had imagekit — new code doesn't
Old template had `{% load imagekit %}`. New template is clean. Old `INSTALLED_APPS` had `imagekit`. New settings don't. Verified: zero imagekit references in new project.

---

## Pending / Next Steps

- [ ] Restart local server after each template change (`Ctrl+C` → `python manage.py runserver`)
- [ ] Download missing media images into `media/menu_images/` (see list above)
- [ ] Test on real phone over local WiFi (use Mac's IP instead of 127.0.0.1)
- [ ] Upload landing video via local admin to test scroll animation
- [ ] Push to GitHub → Render auto-deploys
- [ ] After deploy: verify category groups in admin, confirm all menu items visible
- [ ] **Revoke exposed GitHub token** — `github_pat_11A7KOBYY0wLD...` was pasted in chat

---

## Frontend Details (current state)

### Video scroll animation
- Scroll threshold: `window.innerHeight * 2` (user scrolls 2 screen heights)
- Body height set to `300vh` during landing
- Video scrubs through its duration as user scrolls
- At 95% progress: CTA slides up (pub name + Food/Drinks buttons)
- Hint (logo + "Kaydır" text) disappears immediately on first scroll

### Video CSS
- `position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover`
- Always fills screen edge-to-edge regardless of video aspect ratio or screen size

### Item pages
- All items shown at once — no pagination, pure scroll
- Floating `↑` gold button appears after 300px scroll, one tap returns to top
- Item card: image (4:3) + name + description (3-line clamp) + price
- Tap card → bottom sheet modal with full description and all sizes

---

## Admin Dashboard

URL: `/admin`  
Local credentials: set during `createsuperuser`  
Live credentials: existing `bigapple2025` user (unchanged)

**Dashboard sections:**
- **Kategoriler** — set group (food/drinks), parent, icon, order
- **Menü Ürünleri** — add/edit items and images
- **Kampanya Menüleri** — campaign banners (shown 12:30–16:30)
- **Site Ayarları** — change campaign time window, site title, tagline
- **Landing Video** — upload/replace scroll animation video
- **Promosyon** — popup images shown on page load
