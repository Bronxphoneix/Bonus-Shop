import sqlite3
import random
import string
from datetime import datetime

DB_FILE = "kodemerkezi.db"


def baglanti():
    return sqlite3.connect(DB_FILE)


def tabloları_olustur():
    con = baglanti()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            telegram_id   INTEGER PRIMARY KEY,
            kullanici_adi TEXT,
            ad_soyad      TEXT,
            coin          INTEGER DEFAULT 0,
            kayit_tarihi  TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kodlar (
            kod           TEXT PRIMARY KEY,
            coin_degeri   INTEGER,
            kullanildi_mi INTEGER DEFAULT 0,
            kullanan_id   INTEGER,
            olusturma     TEXT,
            kullanim      TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS islemler (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id   INTEGER,
            tur           TEXT,
            miktar        INTEGER,
            aciklama      TEXT,
            tarih         TEXT
        )
    """)

    con.commit()
    con.close()


def kullanici_kaydet(telegram_id, kullanici_adi, ad_soyad):
    con = baglanti()
    cur = con.cursor()
    cur.execute("SELECT telegram_id FROM kullanicilar WHERE telegram_id=?", (telegram_id,))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO kullanicilar VALUES (?,?,?,?,?)",
            (telegram_id, kullanici_adi, ad_soyad, 0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        con.commit()
        con.close()
        return True  # yeni kayıt
    con.close()
    return False  # zaten kayıtlı


def kullanici_getir(telegram_id):
    con = baglanti()
    cur = con.cursor()
    cur.execute("SELECT * FROM kullanicilar WHERE telegram_id=?", (telegram_id,))
    row = cur.fetchone()
    con.close()
    return row


def coin_ekle(telegram_id, miktar, aciklama=""):
    con = baglanti()
    cur = con.cursor()
    cur.execute("UPDATE kullanicilar SET coin = coin + ? WHERE telegram_id=?", (miktar, telegram_id))
    cur.execute(
        "INSERT INTO islemler (telegram_id, tur, miktar, aciklama, tarih) VALUES (?,?,?,?,?)",
        (telegram_id, "kazanç", miktar, aciklama, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    con.commit()
    con.close()


def kod_olustur(coin_degeri, adet):
    con = baglanti()
    cur = con.cursor()
    uretilen = []
    for _ in range(adet):
        while True:
            kod = "KM-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            cur.execute("SELECT kod FROM kodlar WHERE kod=?", (kod,))
            if not cur.fetchone():
                break
        cur.execute(
            "INSERT INTO kodlar VALUES (?,?,?,?,?,?)",
            (kod, coin_degeri, 0, None, datetime.now().strftime("%Y-%m-%d %H:%M"), None)
        )
        uretilen.append(kod)
    con.commit()
    con.close()
    return uretilen


def kod_kullan(telegram_id, kod):
    con = baglanti()
    cur = con.cursor()
    cur.execute("SELECT * FROM kodlar WHERE kod=?", (kod.upper(),))
    row = cur.fetchone()

    if not row:
        con.close()
        return None, "❌ Geçersiz kod."

    if row[2] == 1:
        con.close()
        return None, "❌ Bu kod daha önce kullanılmış."

    coin_degeri = row[1]
    cur.execute(
        "UPDATE kodlar SET kullanildi_mi=1, kullanan_id=?, kullanim=? WHERE kod=?",
        (telegram_id, datetime.now().strftime("%Y-%m-%d %H:%M"), kod.upper())
    )
    coin_ekle(telegram_id, coin_degeri, f"Kod kullanımı: {kod.upper()}")
    con.commit()
    con.close()
    return coin_degeri, "ok"


def istatistik_getir():
    con = baglanti()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM kullanicilar")
    toplam_kullanici = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM kodlar WHERE kullanildi_mi=0")
    bekleyen_kod = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM kodlar WHERE kullanildi_mi=1")
    kullanilan_kod = cur.fetchone()[0]
    cur.execute("SELECT SUM(coin) FROM kullanicilar")
    toplam_coin = cur.fetchone()[0] or 0
    con.close()
    return toplam_kullanici, bekleyen_kod, kullanilan_kod, toplam_coin
