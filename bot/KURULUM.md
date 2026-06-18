# KodeMerkezi Bot — PC Kurulum Kılavuzu

## 1. Python Kurulumu

1. Tarayıcıdan aç: **https://python.org/downloads**
2. **Download Python 3.11** butonuna tıkla
3. Kurulum ekranında **"Add Python to PATH"** kutusunu işaretle ✅
4. **Install Now** butonuna bas
5. Kurulum bitince CMD aç ve kontrol et:

```
python --version
```

Çıktı şöyle olmalı:
```
Python 3.11.x
```

---

## 2. Bot Dosyalarını İndir

GitHub'dan projeyi indir ya da kopyala. Klasör yapısı şöyle olmalı:

```
KodeMerkezi/
├── bot/
│   ├── bot.py
│   ├── config.py
│   ├── database.py
│   └── requirements.txt
```

---

## 3. Gerekli Kütüphaneyi Kur

CMD'yi aç ve şunu yaz:

```
pip install python-telegram-bot==20.7
```

---

## 4. Config Dosyasını Ayarla

`bot/config.py` dosyasını bir metin editörüyle aç (Notepad yeterli).

### Token Al
BotFather'a git → `/token` yaz → Botunu seç → Token'ı kopyala

### Telegram ID'ni Öğren
Telegram'da `@userinfobot` ara → `/start` yaz → ID'ni not al

### config.py İçeriği

```python
TOKEN = "BURAYA_TOKEN_YAZ"        # BotFather'dan aldığın token

ADMIN_IDS = [
    123456789,                     # Kendi Telegram ID'n
]
```

---

## 5. Botu Başlat

CMD aç, bot klasörüne gir:

```
cd Desktop\KodeMerkezi\bot
python bot.py
```

Ekranda şu yazı çıkarsa bot hazır:

```
✅ Bot çalışıyor...
```

---

## 6. Botu Test Et

Telegram'da botunu bul ve şunları dene:

| Komut | Ne yapar |
|-------|----------|
| `/start` | Kayıt ol, menüyü gör |
| `/bakiye` | Jeton bakiyeni gör |
| `/kod KM-XXXXXXXX` | Kod girerek jeton kazan |
| `/satin_al` | Jeton paketlerini gör |

---

## 7. Yönetici Komutları (Sadece Admin)

| Komut | Örnek | Ne yapar |
|-------|-------|----------|
| `/kod_uret` | `/kod_uret 1000 5` | 5 adet 1000 jetonluk kod üretir |
| `/coin_ekle` | `/coin_ekle 123456789 500` | Kullanıcıya jeton ekler |
| `/kullanici` | `/kullanici 123456789` | Kullanıcı bilgisini gösterir |
| `/istatistik` | `/istatistik` | Genel istatistikleri gösterir |

---

## 8. Sık Karşılaşılan Hatalar

### `python` komutu tanınmıyor
Python kurulumunda **"Add Python to PATH"** işaretlenmemiş.  
Çözüm: Python'u kaldır, tekrar kur ve kutucuğu işaretle.

### `ModuleNotFoundError: telegram`
Kütüphane kurulmamış.  
Çözüm:
```
pip install python-telegram-bot==20.7
```

### `Invalid token`
Token yanlış yapıştırılmış.  
Çözüm: `config.py` dosyasını aç, token'ı başında ve sonunda boşluk olmadan yapıştır.

### Bot cevap vermiyor
`python bot.py` komutu çalışıyor mu kontrol et. CMD'yi kapatırsan bot durur.  
Çözüm: CMD penceresi açık kalmak zorunda.

---

## 9. Botu Sürekli Çalıştır (İsteğe Bağlı)

Bot 7/24 çalışsın istiyorsan bir sunucuya (VPS) kurman gerekir.  
Bunun için ilerleyen aşamada yardım alabilirsin.
