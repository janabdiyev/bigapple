"""
Management command: python manage.py load_menu

Loads all Big Apple Pub menu data (categories + items + sizes)
scraped from the live site. Safe to run multiple times (uses
get_or_create). Run after: python manage.py migrate
"""
from django.core.management.base import BaseCommand
from decimal import Decimal
from menu.models import Category, MenuItem, ItemSize, SiteSettings


FOOD = [
    ('😁 HAPPY HOURS 😁', '😁', 0),
    ('🍔 BURGERS',         '🍔', 1),
    ('SOSİSLİ',            '🌭', 2),
    ('KIZARTMA',           '🍟', 3),
    ('MAIN MENU',          '🍽️', 4),
    ('FISH MENU',          '🐟', 5),
    ('STARTERS',           '🥗', 6),
    ('KAHVALTI',           '🥚', 7),
]

DRINKS_TOP = [
    ('🍺 BİRALAR',  '🍺', 0),
    ('🍹 COCKTAILS','🍹', 1),
    ('ŞARAPLAR',  '🍷', 2),  # parent for wine subcats
    ('ŞİŞELER',   '🍾', 3),
    ('VİSKİLER',  '🥃', 4),
    ('CİNLER',    '🌿', 5),
    ('LİKORLER',  '🍬', 6),
    ('ROMLAR',    '🏝️', 7),
    ('SHOTLAR',   '🥃', 8),
    ('VOTKALAR',  '🧊', 9),
    ('APERATİF',  '🍊', 10),
    ('MEŞRUBAT',  '🥤', 11),
]

WINE_SUBS = [
    ('KIRMIZI ŞARAPLAR',   '🔴', 0),
    ('ROSE ŞARAPLAR',      '🌸', 1),
    ('BEYAZ ŞARAPLAR',     '🤍', 2),
    ('YARI TATLI ŞARAPLAR','🍯', 3),
]

# (category_name, item_name, description, price_or_None, image_or_None, sizes_list_or_None, order)
ITEMS = [
    # HAPPY HOURS
    ('😁 HAPPY HOURS 😁','Kombo Mini Burgers','2-li mini burger + 1 fıçı bira (Carlsberg)\nPzt–Prş 16:30\'a kadar.',499,'menu_items/C8E7C2A9-C0D1-48FA-92BF-E330C72469A0_TVsC6wP.jpeg',None,0),
    ('😁 HAPPY HOURS 😁','Kombo Tavuk Burger','Tavuk Burger + 1 fıçı bira (Carlsberg)\nPzt–Prş 16:30\'a kadar.',499,'menu_items/C8E7C2A9-C0D1-48FA-92BF-E330C72469A0_VYxlxGr.jpeg',None,1),
    ('😁 HAPPY HOURS 😁','Kombo Wrap 06','Tavuk Wrap + 1 fıçı bira (Carlsberg)\nPzt–Prş 16:30\'a kadar.',499,'menu_items/C8E7C2A9-C0D1-48FA-92BF-E330C72469A0.jpeg',None,2),
    # BURGERS
    ('🍔 BURGERS','BIG BOSS','Antrikot et parçaları (150 gr), mevsim yeşilliği, domates, turşu, jalapeno biber, cheddar, karamelize soğan. Parmesan patates ve özel soslar.',750,'menu_images/IMG_4687.jpg',None,0),
    ('🍔 BURGERS','BIG APPLE BURGER','Köfte (180 g), cheddar peynir, Karamelize Soğan, Patates Kızartması, Özel Sos.',650,'menu_images/IMG_6618.JPG',None,1),
    ('🍔 BURGERS','PREMIUM BURGER','Köfte (140g), çift cheddar peynir, dana bacon, patates kızartması ve soslar.',650,'menu_images/IMG_8848.jpeg',None,2),
    ('🍔 BURGERS','MINI BURGER','2 tane mini burger (2x60 g), çift cheddar peyniri, yeşillik, burger sos, patates kızartması.',540,'menu_images/IMG_2525.jpg',None,3),
    ('🍔 BURGERS','IZGARA TAVUK BURGER','Izgara tavuk (150 gr), mevsim yeşilliği, domates, cheddar.',550,'menu_images/WhatsApp_Image_2025-03-24_at_15.33.12.jpg',None,4),
    ('🍔 BURGERS','WRAP 06','Tavuk parçaları (150 gr), kırmızı biber, yeşil biber, kaşar peyniri. Patates kızartması ile servis edilir.',490,'menu_images/Screenshot_2025-12-05_at_21.00.19.png',None,5),
    # SOSİSLİ
    ('SOSİSLİ','HOT DOG','Frankfurter sosis, barbekü sos, parmesan peyniri, anne patatesi ve sos.',650,'menu_images/Screenshot_2025-11-03_at_15.58.41.png',None,0),
    ('SOSİSLİ','LEZZET SARMASI','Mega cheddar dolgulu tereyağlı dana sosis, patates kızartması.',780,'menu_images/Screenshot_2025-11-03_at_15.58.32.png',None,1),
    # KIZARTMA
    ('KIZARTMA','MUNCH COMBO','Dana sosis parçaları, patates kızartması, soğan halkası ve kaşar kroket.',425,'menu_images/Screenshot_2025-11-03_at_15.36.03.png',None,0),
    ('KIZARTMA','CLASSIC COMBO','Tavuk parçaları, patates kızartması, dana sosis, soğan halkası ve kaşar kroket.',850,'menu_images/Screenshot_2025-11-03_at_15.35.51.png',None,1),
    ('KIZARTMA','PERFECT COMBO','Tinders tavuk parçaları, corndog, meksika acılısı, patates kızartması ve soslar.',950,'menu_images/Screenshot_2025-11-03_at_15.37.56.png',None,2),
    ('KIZARTMA','TINDERS TAVUK PARÇASI','Özel soslu tavuk parçaları, patates kızartması ve soslar.',580,'menu_images/Screenshot_2025-11-03_at_15.36.31.png',None,3),
    ('KIZARTMA','MEKSİKA ACILISI','Panelenmiş özel soslu tavuk parçaları, acılı şef patates kızartması ve soslar.',580,'menu_images/Screenshot_2025-11-03_at_15.36.21.png',None,4),
    ('KIZARTMA','CORNDOG','Cheddar dolgulu baby sosis parçaları, patates kızartması ve soslar.',450,'menu_images/Screenshot_2025-11-03_at_15.36.12.png',None,5),
    ('KIZARTMA','TAVUK ŞÖLENİ (2 kişilik)','Tinders tavuk parçaları, patates kızartması, acı, hardal, barbekü, maydonozlu soslar',1050,'menu_images/Screenshot_2025-11-03_at_15.53.16.png',None,6),
    ('KIZARTMA','TAVUK ŞİNİTZEL','Özel karışımla panelenmiş tavuk bonfile, crickle patates tava ve Akdeniz yeşillikleri.',580,'menu_images/Screenshot_2025-11-03_at_15.36.40.png',None,7),
    ('KIZARTMA','ANNEM PATATES','',300,None,None,8),
    ('KIZARTMA','KAŞIK PATATES','',300,None,None,9),
    ('KIZARTMA','CRICKLE PATATES','',300,None,None,10),
    # MAIN MENU (exact live name)
    ('MAIN MENU','ORMAN ESİNTİLİ TAVUK IZGARA','Izgara tavuk, baby patates ve sebze parçaları.',600,'menu_images/Screenshot_2024-12-20_at_13.32.19.png',None,0),
    ('MAIN MENU','MANTAR RÜYALI TAVUK IZGARA','İstiridye mantar soslu ızgara tavuk, baby patates ve sebze parçaları.',650,'menu_images/Screenshot_2024-12-20_at_13.39.14.png',None,1),
    ('MAIN MENU','TAVUK IZGARA','Izgara Tavuk (200 gr), sebzeli basmati pilav, mevsim yeşillikleri.',680,'menu_images/WhatsApp_Image_2024-11-17_at_18.30.45.jpg',None,2),
    ('MAIN MENU','KÖRİ TAVUK','Tavuk, krema, köri baharat, sebzeli pilav.',580,'menu_images/Screenshot_2025-11-03_at_13.16.08.png',None,3),
    ('MAIN MENU','ETLİ DÜRÜM','Antikot et (150 gr), yeşillik, cheddar, kaşar peyniri, domates. Patates kızartması ile.',590,None,None,4),
    ('MAIN MENU','ANNE KÖFTESİ','Izgara dana köftesi, anne patatesi.',550,'menu_images/834f2e8a-f798-4ba8-882a-75bd27a23bc7.jpg',None,5),
    ('MAIN MENU','KÖFTE CRAFT','Anne eli değmiş köfteler, çıtır crickle patates, taze yoğurt ve salçalı sos.',660,'menu_images/Screenshot_2025-11-03_at_15.01.30.png',None,6),
    ('MAIN MENU','BIG ANTRİKOT','Roka, çeri domates, parmesan, turşu, antrikot (200 gr).',750,'menu_images/IMG_6706.jpeg',None,7),
    ('MAIN MENU','DAĞ KEKİKLİ LOKUM','Bonfile dilimleri, baby patates ve sebze parçaları.',1350,'menu_images/Screenshot_2025-11-03_at_14.27.49.png',None,8),
    # NOTE: FETTUCINI ALFREDO was deleted from the live DB on 2026-06-03 — not included
    # FISH MENU (exact live name)
    ('FISH MENU','IZGARA SOMON TABAĞI','Izgara çıtır şekilde pişirilen somon, taze sebzeler, turşu ve limon dilimi.',690,'menu_images/84957411-57e1-4d81-8587-b786f3db2c4e.jpg',None,0),
    # STARTERS (exact live name)
    ('STARTERS','PEYNİR TABAĞI','Rokfor, isli kaşar, gaviera peyniri, taze mevsim meyveleri, ceviz, özel sos ve kreker.',850,'menu_images/peynır_tabagı.jpg',None,0),
    ('STARTERS','Tavuk Salatası','Yeşillik, tavuk kızartması',540,None,None,1),
    ('STARTERS','YEŞİLLİK BAHANE','Maskolin salata, ızgara zeytin, domates, salatalık, ezine peynir.',400,'menu_images/Screenshot_2025-11-03_at_17.30.20.png',None,2),
    ('STARTERS','CRISPY COOL','Kıtır burçak ve fındık kaplamasıyla kızartılmış Maraş dondurması.',570,'menu_images/Screenshot_2025-11-03_at_17.33.46.png',None,3),
    # KAHVALTI
    ('KAHVALTI','KARIŞIK OMLET','Krema ile çırpılmış omlet. Çeri domates, salatalık ve mevsim yeşillikleri.',400,'menu_images/Screenshot_2025-11-03_at_17.40.03.png',None,0),
    ('KAHVALTI','PRATİK KAHVALTI','Akdeniz yeşillikleri, haşlanmış yumurta, ezine peyniri, tulum peyniri, domates, salatalık, zeytin, tam buğday ekmeği.',375,'menu_images/Screenshot_2025-11-03_at_17.39.51.png',None,1),
    # 🍺 BİRALAR (exact live names preserved including typos)
    ('🍺 BİRALAR','FIÇI CARLSBERG','',None,None,[('50 CL','310'),('33 CL','250')],0),
    ('🍺 BİRALAR','TUBORG GOLD','',315,'menu_images/Screenshot_2025-12-05_at_21.15.53.png',None,1),
    ('🍺 BİRALAR','TURBORG FİLTRESİZ','',315,'menu_images/tuborg-filtresiz-bira-atolyesi-kopya.jpg.webp',None,2),
    ('🍺 BİRALAR','TURBORG ICE','',265,None,None,3),
    ('🍺 BİRALAR','EFES MALT 50 CL','',325,None,None,4),
    ('🍺 BİRALAR','EFES GLUTENSİZ','',440,None,None,5),
    ('🍺 BİRALAR','EFES OZEL SERİ 50 CL','',330,None,None,6),
    ('🍺 BİRALAR','EFES PILSEN 50 CL','',330,None,None,7),
    ('🍺 BİRALAR','CARLSBERG 50 CL','',325,None,None,8),
    ('🍺 BİRALAR','CARLSBERG LUNA 50 CL','',335,None,None,9),
    ('🍺 BİRALAR','BOMONTİ FİLTESİZ','',315,None,None,10),
    ('🍺 BİRALAR','BELFAST','',350,None,None,11),
    ('🍺 BİRALAR','BECKS','',365,None,None,12),
    ('🍺 BİRALAR','WEIHENSTEPHANER HEFE WEISS','',380,None,None,13),
    ('🍺 BİRALAR','WEIHENSTEPHANER VITUS','',395,None,None,14),
    ('🍺 BİRALAR','BUD','',370,None,None,15),
    ('🍺 BİRALAR','STELLA','',420,None,None,16),
    ('🍺 BİRALAR','1664 BLANC','',305,None,None,17),
    ('🍺 BİRALAR','AMSTERDAM NAVIGATOR','',540,None,None,18),
    ('🍺 BİRALAR','CORONA','',455,None,None,19),
    ('🍺 BİRALAR','DESPERADOS','',400,None,None,20),
    ('🍺 BİRALAR','DUVEL','',555,None,None,21),
    ('🍺 BİRALAR','MILLER','',None,None,None,22),
    ('🍺 BİRALAR','GUINESS STOUT','',540,None,None,23),
    ('🍺 BİRALAR','ERDINGER','',550,None,None,24),
    ('🍺 BİRALAR','FREDERICK BROWN ALE','',340,None,None,25),
    ('🍺 BİRALAR','FREDERICK INDIA PALE ALE','',340,None,None,26),
    ('🍺 BİRALAR','FREDERICK LOCAL','',340,None,None,27),
    ('🍺 BİRALAR','FREDERICK NEIPA','',340,None,None,28),
    ('🍺 BİRALAR','FREDERICK YAKIMA IPA','',340,None,None,29),
    ('🍺 BİRALAR','3 KAFADAR AMERICAN ALE','',385,None,None,30),
    ('🍺 BİRALAR','3 KAFADAR ASNA VİŞNE','',385,None,None,31),
    ('🍺 BİRALAR','3 KAFADAR BELGIAN BLONDE','',385,None,None,32),
    ('🍺 BİRALAR','3 KAFADAR ENGLISH GOLD','',385,None,None,33),
    ('🍺 BİRALAR','3 KAFADAR GECE STOUT','',385,None,None,34),
    ('🍺 BİRALAR','3 KAFADAR MANGO','',385,None,None,35),
    ('🍺 BİRALAR','3 KAFADAR MOSAIC IPA','',385,None,None,36),
    ('🍺 BİRALAR','3 KAFADAR OKTO','',385,None,None,37),
    ('🍺 BİRALAR','3 KAFADAR PEŞPEŞE ŞEFTALİ','',385,None,None,38),
    ('🍺 BİRALAR','3 KAFADAR STARDUST NEIPA','',385,None,None,39),
    ('🍺 BİRALAR','3 KAFADAR TÜTSÜ','',385,None,None,40),
    ('🍺 BİRALAR','BLUE MOON','',360,None,None,41),
    ('🍺 BİRALAR','BUDWEISSER','',375,None,None,42),
    ('🍺 BİRALAR','DAURA GLUTENSİZ','',375,None,None,43),
    ('🍺 BİRALAR','HEINEKEN','',360,None,None,44),
    ('🍺 BİRALAR','KIRIN ICHIBAN','',360,None,None,45),
    ('🍺 BİRALAR','PAULANER WEISS','',360,None,None,46),
    ('🍺 BİRALAR','ESTRELLA','',360,None,None,47),
    # 🍹 COCKTAILS (exact live name)
    ('🍹 COCKTAILS','007 VESPER MARTİNİ','Cin, Vodka, Lillet Blanc',820,None,None,0),
    ('🍹 COCKTAILS','APEROL SPRITZ','Beyaz Şarap, Aperol, Soda',645,None,None,1),
    ('🍹 COCKTAILS','BIG LONG ISLAND','Vodka, Tekila, Cin, Rom, Portakal Likörü, Limon Suyu, Cola',1050,'menu_images/Screenshot_2025-12-05_at_12.45.15.png',None,2),
    ('🍹 COCKTAILS','BMW','Baileys, Malibu, Whisky',695,None,None,3),
    ('🍹 COCKTAILS','CHALLENGER','Vodka, Tekila, Cin, Çilek, Limon Suyu.',930,'menu_images/Screenshot_2025-12-05_at_12.58.52.png',None,4),
    ('🍹 COCKTAILS','CUBA LIBRE','Rom, Limon Suyu, Cola.',700,None,None,5),
    ('🍹 COCKTAILS','DRAGON JAM','Jameson, Safari, Limon Suyu, Dragon meyvesi, Tarçın.',740,None,None,6),
    ('🍹 COCKTAILS','DRY MARTİNİ','Cin, Martini Dry, Garnish zeytin.',610,None,None,7),
    ('🍹 COCKTAILS','FLAMINGO','Rom, Limonce, Campari, Çilek, Yumurta Akı, Esmer Şeker',630,None,None,8),
    ('🍹 COCKTAILS','GARİBALDİ','Campari, Gerçek Portakal Suyu',650,None,None,9),
    ('🍹 COCKTAILS','GIN FIZZ','Cin, Limon Suyu, Soda.',590,None,None,10),
    ('🍹 COCKTAILS','GIN TONİK','Cin, Limon Suyu, Schweppes Tonic',590,None,None,11),
    ('🍹 COCKTAILS','GOD FATHER','Whisky, Disaronno.',690,None,None,12),
    ('🍹 COCKTAILS','INFERNO','Rom, Martini Extra Dry, Safari, Çarkıfelek Meyvesi.',880,None,None,13),
    ('🍹 COCKTAILS','JAGGER BOMB','Jaggermeister, Redbull',590,None,None,14),
    ('🍹 COCKTAILS','KIWI SMASH','Vodka, Martini Bianco, Limon Suyu, Kiwi',640,'menu_images/Screenshot_2025-12-05_at_12.43.18.png',None,15),
    ('🍹 COCKTAILS','KUZU KULAĞI GIN','Cin, Portakal Likörü, Kuzu Kulağı, Limon Suyu',660,'menu_images/Screenshot_2025-12-05_at_13.00.55.png',None,16),
    ('🍹 COCKTAILS','LYNCHBURG LEMONADE','Whisky, Portakal Likörü, Angostura Bitter, Limon Suyu, Sprite',750,'menu_images/Screenshot_2025-12-05_at_12.48.09.png',None,17),
    ('🍹 COCKTAILS','MANGO MİRAGE','Vodka, Rom, Tekila, Aperol, Mango Püresi, Limon Suyu.',920,None,None,18),
    ('🍹 COCKTAILS','MANHATTAN','Whiskey, Martini Rosso, Angostura Bitter',700,None,None,19),
    ('🍹 COCKTAILS','MARGARİTA','Tekila, Portakal Likörü, Limon Suyu',700,'menu_images/Screenshot_2025-12-05_at_12.55.18.png',None,20),
    ('🍹 COCKTAILS','MİNTY GOLD','Whisky, Limonce, Branca Menta.',770,None,None,21),
    ('🍹 COCKTAILS','MOJİTO','Rom, Nane, Limon Suyu, Soda.',645,'menu_images/Screenshot_2025-12-05_at_12.53.55.png',None,22),
    ('🍹 COCKTAILS','NARLI MARGARİTA','Tekila, Portakal Likörü, Limon Suyu, Çilek',710,None,None,23),
    ('🍹 COCKTAILS','NEGRONI','Cin, Martini Rosso, Campari',750,None,None,24),
    ('🍹 COCKTAILS','PORN STAR MARTİNİ','Vanilla Vodka, Martini Bianco, Passoa, Limon Suyu, Çarkıfelek Meyvesi',800,'menu_images/Screenshot_2025-12-05_at_12.50.19.png',None,25),
    ('🍹 COCKTAILS','ROYAL SEA','Whisky, Safari, Çarkıfelek Meyvesi, Chambord, Limon Suyu.',950,None,None,26),
    ('🍹 COCKTAILS','THUNDER MALIBU','Malibu, Limon Suyu, Esmer Şeker, Soda',620,None,None,27),
    ('🍹 COCKTAILS','VİRGİN ANGEL','Cin, Vodka, Portakal Likörü, Fesleğen, Limon Suyu, Sprite.',900,None,None,28),
    ('🍹 COCKTAILS','VODKA MARTİNİ','Vodka, Martini Dry',620,None,None,29),
    ('🍹 COCKTAILS','VODKA TONİK','Vodka, Schweppes Tonic',590,None,None,30),
    ('🍹 COCKTAILS','WHISKEY SOUR','Whisky, Limon Suyu, Esmer Şeker, yumurta akı',750,'menu_images/Screenshot_2025-12-05_at_12.47.25.png',None,31),
    ('🍹 COCKTAILS','YILDIRIM','Gin, Triple sec, Salatalık, Limon suyu, Portakal Suyu',590,None,None,32),
    # WINES (subcategories)
    ('KIRMIZI ŞARAPLAR','VİNKARA QUATTRO KIRMIZI','',None,None,[('KADEH','360'),('SİSE','1440')],0),
    ('KIRMIZI ŞARAPLAR','VİNKARA CABARNET SAUVIGNON','',None,None,[('KADEH','405'),('SİSE','1650')],1),
    ('KIRMIZI ŞARAPLAR','VİNKARA KALECİK KARASI','',None,None,[('KADEH','405'),('25 CL','675'),('SİSE','1650')],2),
    ('KIRMIZI ŞARAPLAR','VİNKARA MERLOT','',None,None,[('KADEH','405'),('SİSE','1650')],3),
    ('KIRMIZI ŞARAPLAR','VİNKARA SYRAH','',None,None,[('KADEH','405'),('SİSE','1650')],4),
    ('KIRMIZI ŞARAPLAR','VİNKARA ÖKÜZGÖZÜ BOĞAZKERE','',None,None,[('KADEH','405'),('SİSE','1650')],5),
    ('KIRMIZI ŞARAPLAR','VİNKARA ATELİER ÖKÜZGÖZÜ','',None,None,[('KADEH','475'),('SİSE','1900')],6),
    ('KIRMIZI ŞARAPLAR','VİNKARA RESERVE CABARNET SAUVIGNON','',None,None,[('KADEH','790'),('SİSE','3100')],7),
    ('KIRMIZI ŞARAPLAR','VİNKARA RESERVE KALECİK KARASI','',None,None,[('KADEH','750'),('SİSE','3000')],8),
    ('KIRMIZI ŞARAPLAR','VİNKARA RESERVE MERLOT','',None,None,[('SİSE','3100')],9),
    ('KIRMIZI ŞARAPLAR','VİNKARA GRAND RESERVE BOĞAZKERE','',None,None,[('SİSE','3100')],10),
    ('KIRMIZI ŞARAPLAR','VİNKARA RESERVE CMS','',None,None,[('SİSE','3100')],11),
    ('KIRMIZI ŞARAPLAR','VİNKARA İMZA 23 RPB 7 Lİ KUPAJ','',None,None,[('SİSE','4000')],12),
    ('KIRMIZI ŞARAPLAR','VİNKARA GRAND RESERVE ALBERELLO KALECİK KARASI','',None,None,[('SİSE','5800')],13),
    ('ROSE ŞARAPLAR','VİNKARA QUATTRO PEMBE','',None,None,[('KADEH','360'),('SİSE','1440')],0),
    ('ROSE ŞARAPLAR','VİNKARA MİNOJ KALECİK KARASI','',None,None,[('KADEH','405'),('25 CL','675'),('SİSE','1650')],1),
    ('ROSE ŞARAPLAR','VİNKARA ATELİER KALECİK KARASI - ÖKÜZGÖZÜ','',None,None,[('KADEH','505'),('SİSE','2100')],2),
    ('ROSE ŞARAPLAR','VİNKARA ATELİER KALECİK KARASI','',None,None,[('KADEH','505'),('SİSE','2100')],3),
    ('BEYAZ ŞARAPLAR','VİNKARA QUATTRO BEYAZ','',None,None,[('KADEH','360'),('SİSE','1440')],0),
    ('BEYAZ ŞARAPLAR','VİNKARA ATELİER HASANDEDE','',None,None,[('KADEH','505'),('25 CL','750'),('SİSE','2000')],1),
    ('BEYAZ ŞARAPLAR','VİNKARA ATELİER KALECİK KARASI BLANC DE NOİR','',None,None,[('KADEH','505'),('SİSE','2000')],2),
    ('BEYAZ ŞARAPLAR','VİNKARA NARİNCE','',None,None,[('KADEH','425'),('SİSE','1700')],3),
    ('BEYAZ ŞARAPLAR','VİNKARA SAUVIGNON BLANC','',None,None,[('KADEH','500'),('SİSE','2000')],4),
    ('BEYAZ ŞARAPLAR','VİNKARA RİESLİNG','',None,None,[('KADEH','585'),('SİSE','2350')],5),
    ('BEYAZ ŞARAPLAR','VİNKARA RESERVE NARİNCE','',None,None,[('KADEH','750'),('SİSE','3000')],6),
    ('YARI TATLI ŞARAPLAR','VİNKARA DÖMİ-SEK BORNOVA MİSKETİ BEYAZ','',None,None,None,0),
    ('YARI TATLI ŞARAPLAR','VİNKARA KIRMIZI ATELİER KALECİK KARASI','',None,None,[('KADEH','505'),('SİSE','2000')],1),
    # ŞİŞELER
    ('ŞİŞELER','BEEFEATER','',None,None,[('35 CL','2700'),('70 CL','4500')],0),
    ('ŞİŞELER','CHIVAS REGAL','',None,None,[('70 CL','5000')],1),
    ('ŞİŞELER','GORDONS GIN','',None,None,[('35 CL','2500'),('70 CL','4200')],2),
    ('ŞİŞELER','JAMESON','',None,None,[('70 CL','4500')],3),
    ('ŞİŞELER','JAMESON BLACK BARREL','',None,None,[('70 CL','5500')],4),
    ('ŞİŞELER','JOHNNIE WALKER BLACK LABEL','',None,None,[('70 CL','4700')],5),
    # VİSKİLER
    ('VİSKİLER','J.W. BLACK LABEL','',None,None,[('5 CL','475'),('8 CL','800')],0),
    ('VİSKİLER','J.W. BLACK RUBY','',None,None,[('3 CL','480'),('5 CL','650')],1),
    ('VİSKİLER','J.W. DOUBLE BLACK LABEL','',None,None,[('5 CL','550'),('8 CL','750')],2),
    ('VİSKİLER','CHIVAS REGAL 12','',None,None,[('5 CL','500'),('8 CL','700')],3),
    ('VİSKİLER','CHIVAS REGAL SMOKY','',None,None,[('5 CL','520'),('8 CL','710')],4),
    ('VİSKİLER','CHIVAS REGAL 15','',None,None,[('5 CL','675'),('8 CL','900')],5),
    ('VİSKİLER','CHIVAS REGAL 18','',None,None,[('5 CL','800'),('8 CL','1100')],6),
    ('VİSKİLER',"JACK DANIEL'S NO. 7",'',None,None,[('5 CL','500'),('8 CL','700')],7),
    ('VİSKİLER',"JACK DANIEL'S APPLE",'',None,None,[('5 CL','500'),('8 CL','700')],8),
    ('VİSKİLER',"JACK DANIEL'S HONEY",'',None,None,[('5 CL','500'),('8 CL','700')],9),
    ('VİSKİLER',"JACK DANIEL'S SINGLE BARREL",'',None,None,[('5 CL','650'),('8 CL','900')],10),
    ('VİSKİLER','DIMPLE GOLDEN SELECTION','',None,None,[('5 CL','500'),('8 CL','700')],11),
    ('VİSKİLER','JAMESON','',None,None,[('5 CL','440'),('8 CL','600')],12),
    ('VİSKİLER','JAMESON BLACK BARREL','',None,None,[('5 CL','510'),('8 CL','700')],13),
    ('VİSKİLER','MONKEY SHOULDERS','',None,None,[('5 CL','520'),('8 CL','740')],14),
    ('VİSKİLER','TULLAMORE','',None,None,[('5 CL','450'),('8 CL','650')],15),
    ('VİSKİLER','BANKHALL','',None,None,[('5 CL','400'),('8 CL','600')],16),
    ('VİSKİLER','GLENLIVET FOUNDERS RESERVE','',None,None,[('5 CL','500'),('8 CL','700')],17),
    ('VİSKİLER','GLENLIVET 12','',None,None,[('5 CL','560'),('8 CL','770')],18),
    ('VİSKİLER','SINGLETON','',None,None,[('5 CL','500'),('8 CL','700')],19),
    ('VİSKİLER','GLENFIDDICH 12','',None,None,[('5 CL','580'),('8 CL','800')],20),
    ('VİSKİLER','CARDHU 15','',None,None,[('5 CL','520'),('8 CL','710')],21),
    ('VİSKİLER','ABERLOUR 12','',None,None,[('5 CL','600'),('8 CL','800')],22),
    ('VİSKİLER','GLENKINCHE 12','',None,None,[('5 CL','600'),('8 CL','800')],23),
    ('VİSKİLER','LAGAVULIN 8','',None,None,[('5 CL','600'),('8 CL','800')],24),
    ('VİSKİLER','LAGAVULIN 12','',None,None,[('5 CL','1000'),('8 CL','1400')],25),
    ('VİSKİLER','LAGAVULIN 16','',None,None,[('5 CL','1400'),('8 CL','2000')],26),
    ('VİSKİLER','TALISKER 8','',None,None,[('5 CL','600'),('8 CL','800')],27),
    ('VİSKİLER','TALISKER 10','',None,None,[('5 CL','620'),('8 CL','840')],28),
    ('VİSKİLER','MACALLAN 12','',None,None,[('5 CL','800'),('8 CL','1100')],29),
    ('VİSKİLER','COAL ILA 12','',None,None,[('5 CL','650'),('8 CL','900')],30),
    # CİNLER
    ('CİNLER','BEEFEATER LONDON DRY','',None,None,[('5 CL','450'),('8 CL','660')],0),
    ('CİNLER','BEEFEATER PINK','',None,None,[('5 CL','460'),('8 CL','690')],1),
    ('CİNLER','FORDS LONDON DRY','',None,None,[('5 CL','600'),('8 CL','900')],2),
    ('CİNLER','GORDONS LONDON DRY','',None,None,[('5 CL','440'),('8 CL','650')],3),
    ('CİNLER','GORDONS PINK','',None,None,[('5 CL','450'),('8 CL','660')],4),
    ('CİNLER','GORDONS SICILLIAN LEMONADE','',None,None,[('5 CL','450'),('8 CL','660')],5),
    ('CİNLER','HENDRICKS','',None,None,[('5 CL','650'),('8 CL','900')],6),
    ('CİNLER','MALFY GIN','',None,None,[('5 CL','520'),('8 CL','780')],7),
    ('CİNLER','MALFY LIMONADE','',None,None,[('5 CL','520'),('8 CL','780')],8),
    ('CİNLER','MALFY ROSE','',None,None,[('5 CL','520'),('8 CL','780')],9),
    ('CİNLER','MOSAIC GIN','',None,None,[('5 CL','550'),('8 CL','800')],10),
    ('CİNLER','TANQUERAY LONDON DRY','',None,None,[('5 CL','550'),('8 CL','750')],11),
    ('CİNLER','TANQUERAY NO TEN','',None,None,[('5 CL','640'),('8 CL','880')],12),
    # LİKORLER
    ('LİKORLER','BAILEYS','',None,None,[('SHOT','300'),('5 CL','375')],0),
    ('LİKORLER','DISSARONNA','',None,None,[('SHOT','300'),('5 CL','375')],1),
    ('LİKORLER','JAGERMEISTER','',None,None,[('SHOT','300'),('5 CL','375')],2),
    ('LİKORLER','KAHLUA','',None,None,[('SHOT','300'),('5 CL','375')],3),
    ('LİKORLER','SAFARI','',None,None,[('SHOT','300'),('5 CL','375')],4),
    ('LİKORLER','VALHALLA','',None,None,[('SHOT','300'),('5 CL','375')],5),
    # ROMLAR
    ('ROMLAR','BUMBU VANILLA','',None,None,[('5 CL','550'),('8 CL','750')],0),
    ('ROMLAR','CAPTAIN MORGAN SPICED','',None,None,[('5 CL','450'),('8 CL','650')],1),
    ('ROMLAR','CAPTAINMORGAN WHITE','',None,None,[('5 CL','450'),('8 CL','650')],2),
    # SHOTLAR
    ('SHOTLAR','ASTRAL TEKİLA','',220,None,None,0),
    ('SHOTLAR','DON JULIO BIANCO SHOT','',380,None,None,1),
    ('SHOTLAR','DON JULIO REPOSADO','',390,None,None,2),
    ('SHOTLAR','OLMECA ALTOS PLATA','',270,None,None,3),
    ('SHOTLAR','OLMECA GOLD SHOT','',260,None,None,4),
    ('SHOTLAR','OLMECA SILVER SHOT','',250,None,None,5),
    # VOTKALAR
    ('VOTKALAR','ABSOLUT','',None,None,[('5 CL','450'),('8 CL','650')],0),
    ('VOTKALAR','ABSOLUT EXTRAT','',None,None,[('5 CL','450'),('8 CL','650')],1),
    ('VOTKALAR','ABSOLUT MANDARIN','',None,None,[('5 CL','450'),('8 CL','650')],2),
    ('VOTKALAR','ABSOLUT VANLLA','',None,None,[('5 CL','450'),('8 CL','650')],3),
    ('VOTKALAR','BELVEDERE','',None,None,[('5 CL','800'),('8 CL','1100')],4),
    ('VOTKALAR','KETEL ONE','',None,None,[('5 CL','800'),('8 CL','1100')],5),
    ('VOTKALAR','SMIRNOFF','',None,None,[('5 CL','430'),('8 CL','630')],6),
    # APERATİF
    ('APERATİF','APEROL','',None,None,[('SHOT','300'),('5 CL','375')],0),
    ('APERATİF','CAMPARİ','',None,None,[('5 CL','300'),('8 CL','375')],1),
    ('APERATİF','LIMONCE','',None,None,[('SHOT','300'),('5 CL','375')],2),
    ('APERATİF','MARTINI BIANCO','',None,None,[('SHOT','300'),('5 CL','375')],3),
    ('APERATİF','MARTINI EXTRA DRY','',None,None,[('SHOT','300'),('5 CL','375')],4),
    ('APERATİF','SAMBUCA','',None,None,[('SHOT','300'),('5 CL','375')],5),
    # MEŞRUBAT
    ('MEŞRUBAT','ALKOLSUZ BİRA BITBURGER','',285,None,None,0),
    ('MEŞRUBAT','ALKOLSÜZ MOJİTO','',350,None,None,1),
    ('MEŞRUBAT','AYRAN 30 CL','',140,None,None,2),
    ('MEŞRUBAT','CHURCHILL','',145,None,None,3),
    ('MEŞRUBAT','COLA CLASSIC','',110,None,None,4),
    ('MEŞRUBAT','COLA LIGHT','',110,None,None,5),
    ('MEŞRUBAT','COLA ZERO','',110,None,None,6),
    ('MEŞRUBAT','FANTA','',110,None,None,7),
    ('MEŞRUBAT','FUSE TEA KARPUZ','',110,None,None,8),
    ('MEŞRUBAT','FUSE TEA LİMON','',110,None,None,9),
    ('MEŞRUBAT','FUSE TEA MANGO ANANAS','',110,None,None,10),
    ('MEŞRUBAT','FUSE TEA ŞEFTALİ','',110,None,None,11),
    ('MEŞRUBAT','GERÇEK PORTAKAL SUYU','',220,None,None,12),
    ('MEŞRUBAT','NESCAFE','',120,None,None,13),
    ('MEŞRUBAT','ORJİNAL LİMONATA (NANELİ)','',200,None,None,14),
    ('MEŞRUBAT','ORJİNAL NARLI LİMONATA','',240,None,None,15),
    ('MEŞRUBAT','Red Bull Classic','',150,None,None,16),
    ('MEŞRUBAT','Red Bull Sugarfree','',150,None,None,17),
    ('MEŞRUBAT','SCHWEPPES LİMON 25 CL','',120,None,None,18),
    ('MEŞRUBAT','SCHWEPPES TONIK 25 CL','',120,None,None,19),
    ('MEŞRUBAT','SCHWEPPES TONİK MANDARIN 25 CL','',120,None,None,20),
    ('MEŞRUBAT','SODA BEYPAZARI','',80,None,None,21),
    ('MEŞRUBAT','SPRİTE','',110,None,None,22),
    ('MEŞRUBAT','SU','',40,None,None,23),
    ('MEŞRUBAT','TURK KAHVESİ','',None,None,None,24),
    ('MEŞRUBAT','VİŞNE SUYU','',110,None,None,25),
    ('MEŞRUBAT','ÇAY','',100,None,None,26),
]


class Command(BaseCommand):
    help = 'Load all Big Apple Pub menu data from live site scrape'

    def handle(self, *args, **options):
        self.stdout.write('Loading categories...')
        cat_map = {}

        # Food
        for name, icon, order in FOOD:
            c, created = Category.objects.get_or_create(
                name=name,
                defaults={'group': 'food', 'icon': icon, 'order': order}
            )
            if not created:
                c.group = 'food'; c.icon = icon; c.order = order; c.save()
            cat_map[name] = c

        # Drinks top-level
        for name, icon, order in DRINKS_TOP:
            c, created = Category.objects.get_or_create(
                name=name,
                defaults={'group': 'drinks', 'icon': icon, 'order': order}
            )
            if not created:
                c.group = 'drinks'; c.icon = icon; c.order = order; c.save()
            cat_map[name] = c

        # Wine subcategories
        wine_parent = cat_map['ŞARAPLAR']
        for name, icon, order in WINE_SUBS:
            c, created = Category.objects.get_or_create(
                name=name,
                defaults={'group': 'drinks', 'icon': icon, 'order': order, 'parent': wine_parent}
            )
            if not created:
                c.group = 'drinks'; c.icon = icon; c.order = order; c.parent = wine_parent; c.save()
            cat_map[name] = c

        self.stdout.write(f'  {Category.objects.count()} categories ready')

        # Site settings
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_title='BIG APPLE PUB',
                tagline='Taze, bol ve sipariş üzerine!',
                campaign_enabled=True,
                campaign_start='12:30',
                campaign_end='16:30',
            )

        # Items
        self.stdout.write('Loading menu items...')
        created_count = 0
        for row in ITEMS:
            cat_name, name, desc, price, img, sizes, order = row
            cat = cat_map.get(cat_name)
            if not cat:
                self.stdout.write(f'  WARN: missing cat "{cat_name}"')
                continue

            item, created = MenuItem.objects.get_or_create(
                name=name, category=cat,
                defaults={'description': desc or '', 'order': order}
            )
            if not created:
                item.description = desc or ''
                item.order = order

            if price is not None:
                item.price = Decimal(str(price))
            if img:
                item.image = img
            item.save()

            if sizes:
                ItemSize.objects.filter(item=item).delete()
                for i, (qty, p) in enumerate(sizes):
                    ItemSize.objects.create(item=item, qty=qty, price=Decimal(str(p)), order=i)

            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! {MenuItem.objects.count()} items, '
            f'{ItemSize.objects.count()} sizes, '
            f'{created_count} new items created.'
        ))
