# Bonus Shop — KodeMerkezi Gaming Platform

Sosyal gaming platformu. Kullanıcılar jeton satın alır, oyun oynar, Telegram botu üzerinden kod kullanır.

## Proje Yapısı

```
Bonus-Shop/
├── bot/
│   ├── bot.py            → Telegram bot (ana dosya)
│   ├── config.py         → Token ve admin ayarları
│   ├── database.py       → SQLite veritabanı işlemleri
│   ├── requirements.txt  → Python kütüphaneleri
│   ├── kurulum.bat       → Windows otomatik kurulum
│   └── KURULUM.md        → Kurulum kılavuzu
└── slot/
    └── pragmatic-play/
        ├── index.html    → Oyun sitesi (TR/EN çift dilli)
        ├── style.css     → Tasarım
        └── app.js        → Oyun listesi ve dil sistemi
```

---

## Telegram Bot

### Kullanıcı Komutları
| Komut | Açıklama |
|-------|----------|
| `/start` | Kayıt ol, menüyü gör |
| `/bakiye` | Jeton bakiyeni gör |
| `/kod KM-XXXXXXXX` | Kod girerek jeton kazan |
| `/satin_al` | Jeton paketlerini gör |

### Yönetici Komutları
| Komut | Örnek | Açıklama |
|-------|-------|----------|
| `/kod_uret` | `/kod_uret 1000 5` | 5 adet 1000 jetonluk kod üretir |
| `/coin_ekle` | `/coin_ekle 123456789 500` | Kullanıcıya jeton ekler |
| `/kullanici` | `/kullanici 123456789` | Kullanıcı bilgisini gösterir |
| `/istatistik` | `/istatistik` | Genel istatistikleri gösterir |

---

## Kurulum

### 1. Otomatik (Windows)
```
bot/kurulum.bat dosyasını çift tıkla
```

### 2. Manuel
```
pip install python-telegram-bot --upgrade
```

### 3. Config Ayarla
`bot/config.py` dosyasını aç:
```python
TOKEN = "BotFather'dan aldığın token"
ADMIN_IDS = [Telegram_ID]
```

### 4. Başlat
```
cd bot
python bot.py
```

---

## Oyun Sitesi

**Canlı önizleme:**
```
https://htmlpreview.github.io/?https://github.com/Bronxphoneix/Bonus-Shop/blob/claude/site-viewing-location-12vr0i/slot/pragmatic-play/index.html
```

- TR / EN dil desteği (header'daki butonla değişir)
- 30 Pragmatic Play oyunu
- Filtreler: Tümü, Popüler, Yeni, Megaways, Bonus, Jackpot
- Arama ve sıralama

---

## Sonraki Adımlar

- [ ] Oyun sitesini bota bağla (web app entegrasyonu)
- [ ] Mobcash ödeme entegrasyonu
- [ ] VPS'e taşı (7/24 çalışsın)
- [ ] Kullanıcı paneli ekle
- [ ] Gerçek oyun motoru entegrasyonu

---

## Branch
Geliştirme: `claude/site-viewing-location-12vr0i`
