from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)
from config import TOKEN, ADMIN_IDS, COIN_PACKAGES
import database as db

db.tabloları_olustur()


def admin_mi(telegram_id):
    return telegram_id in ADMIN_IDS


# ─── /start ───────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    yeni = db.kullanici_kaydet(user.id, user.username or "", user.full_name)

    if yeni:
        mesaj = (
            f"👋 Hoş geldin, {user.first_name}!\n\n"
            "🎮 KodeMerkezi Gaming'e kayıt oldun.\n"
            "💰 Başlangıç coinin: 0\n\n"
            "Kod girerek veya paket satın alarak coin kazanabilirsin."
        )
    else:
        kullanici = db.kullanici_getir(user.id)
        mesaj = (
            f"👋 Tekrar hoş geldin, {user.first_name}!\n\n"
            f"💰 Coin bakiyen: {kullanici[3]:,}"
        )

    klavye = [
        [InlineKeyboardButton("💰 Bakiyem", callback_data="bakiye"),
         InlineKeyboardButton("🎟 Kod Gir", callback_data="kod_gir")],
        [InlineKeyboardButton("🛒 Coin Satın Al", callback_data="satin_al")],
    ]
    await update.message.reply_text(mesaj, reply_markup=InlineKeyboardMarkup(klavye))


# ─── /bakiye ──────────────────────────────────────────────
async def bakiye(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kullanici = db.kullanici_getir(update.effective_user.id)
    if not kullanici:
        await update.message.reply_text("Önce /start yaz.")
        return
    await update.message.reply_text(f"💰 Coin bakiyen: {kullanici[3]:,}")


# ─── /kod ─────────────────────────────────────────────────
async def kod(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Kullanım: /kod KM-XXXXXXXX")
        return

    girilen_kod = ctx.args[0].strip()
    kullanici = db.kullanici_getir(update.effective_user.id)
    if not kullanici:
        await update.message.reply_text("Önce /start yaz.")
        return

    coin, sonuc = db.kod_kullan(update.effective_user.id, girilen_kod)
    if sonuc == "ok":
        await update.message.reply_text(
            f"✅ Kod başarıyla kullanıldı!\n"
            f"💰 +{coin:,} coin eklendi.\n"
            f"💳 Yeni bakiyen: {db.kullanici_getir(update.effective_user.id)[3]:,}"
        )
    else:
        await update.message.reply_text(sonuc)


# ─── /satin-al ────────────────────────────────────────────
async def satin_al(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    mesaj = "🛒 *Coin Paketleri*\n\n"
    for p in COIN_PACKAGES:
        mesaj += f"🎮 *{p['isim']}*\n💰 {p['coin']:,} Coin — {p['fiyat']}\n\n"
    mesaj += "Satın almak için bir admin ile iletişime geç."
    await update.message.reply_text(mesaj, parse_mode="Markdown")


# ─── ADMIN: /kod-uret ─────────────────────────────────────
async def kod_uret(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not admin_mi(update.effective_user.id):
        await update.message.reply_text("❌ Bu komut sadece adminlere özel.")
        return

    if len(ctx.args) != 2:
        await update.message.reply_text("Kullanım: /kod-uret <coin_miktarı> <adet>\nÖrnek: /kod-uret 1000 5")
        return

    try:
        coin = int(ctx.args[0])
        adet = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("❌ Geçersiz değer. Sayı gir.")
        return

    if adet > 50:
        await update.message.reply_text("❌ Tek seferde max 50 kod üretilebilir.")
        return

    kodlar = db.kod_olustur(coin, adet)
    mesaj = f"✅ {adet} adet, {coin:,} coinlik kod üretildi:\n\n"
    mesaj += "\n".join(f"`{k}`" for k in kodlar)
    await update.message.reply_text(mesaj, parse_mode="Markdown")


# ─── ADMIN: /kullanici ────────────────────────────────────
async def kullanici_bilgi(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not admin_mi(update.effective_user.id):
        await update.message.reply_text("❌ Bu komut sadece adminlere özel.")
        return

    if not ctx.args:
        await update.message.reply_text("Kullanım: /kullanici <telegram_id>")
        return

    try:
        hedef_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ Geçersiz ID.")
        return

    k = db.kullanici_getir(hedef_id)
    if not k:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    await update.message.reply_text(
        f"👤 *Kullanıcı Bilgisi*\n\n"
        f"ID: `{k[0]}`\n"
        f"Kullanıcı adı: @{k[1]}\n"
        f"Ad: {k[2]}\n"
        f"💰 Coin: {k[3]:,}\n"
        f"📅 Kayıt: {k[4]}",
        parse_mode="Markdown"
    )


# ─── ADMIN: /istatistik ───────────────────────────────────
async def istatistik(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not admin_mi(update.effective_user.id):
        await update.message.reply_text("❌ Bu komut sadece adminlere özel.")
        return

    t_k, b_k, k_k, t_c = db.istatistik_getir()
    await update.message.reply_text(
        f"📊 *İstatistikler*\n\n"
        f"👥 Toplam kullanıcı: {t_k}\n"
        f"🎟 Bekleyen kod: {b_k}\n"
        f"✅ Kullanılan kod: {k_k}\n"
        f"💰 Toplam coin: {t_c:,}",
        parse_mode="Markdown"
    )


# ─── ADMIN: /coin-ekle ────────────────────────────────────
async def coin_ekle_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not admin_mi(update.effective_user.id):
        await update.message.reply_text("❌ Bu komut sadece adminlere özel.")
        return

    if len(ctx.args) != 2:
        await update.message.reply_text("Kullanım: /coin-ekle <telegram_id> <miktar>")
        return

    try:
        hedef_id = int(ctx.args[0])
        miktar = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("❌ Geçersiz değer.")
        return

    k = db.kullanici_getir(hedef_id)
    if not k:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    db.coin_ekle(hedef_id, miktar, "Admin tarafından eklendi")
    yeni = db.kullanici_getir(hedef_id)
    await update.message.reply_text(
        f"✅ {k[2]} ({hedef_id}) kullanıcısına {miktar:,} coin eklendi.\n"
        f"💰 Yeni bakiye: {yeni[3]:,}"
    )


# ─── CALLBACK ─────────────────────────────────────────────
async def callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "bakiye":
        k = db.kullanici_getir(query.from_user.id)
        await query.message.reply_text(f"💰 Coin bakiyen: {k[3]:,}" if k else "Önce /start yaz.")

    elif data == "kod_gir":
        await query.message.reply_text("Kodu girmek için:\n/kod KM-XXXXXXXX")

    elif data == "satin_al":
        mesaj = "🛒 *Coin Paketleri*\n\n"
        for p in COIN_PACKAGES:
            mesaj += f"🎮 *{p['isim']}*\n💰 {p['coin']:,} Coin — {p['fiyat']}\n\n"
        mesaj += "Satın almak için bir admin ile iletişime geç."
        await query.message.reply_text(mesaj, parse_mode="Markdown")


# ─── MAIN ─────────────────────────────────────────────────
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bakiye", bakiye))
    app.add_handler(CommandHandler("kod", kod))
    app.add_handler(CommandHandler("satin_al", satin_al))
    app.add_handler(CommandHandler("kod_uret", kod_uret))
    app.add_handler(CommandHandler("kullanici", kullanici_bilgi))
    app.add_handler(CommandHandler("istatistik", istatistik))
    app.add_handler(CommandHandler("coin_ekle", coin_ekle_admin))
    app.add_handler(CallbackQueryHandler(callback))

    print("✅ Bot çalışıyor...")
    app.run_polling()
