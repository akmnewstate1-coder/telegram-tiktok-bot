import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes
)

TOKEN = "8597226820:AAEUk6asQ-JeP2WSr5Hg2IGucySkzDApOks"

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = update.message.text

        # Cek apakah link TikTok
        if "tiktok.com" not in url and "vt.tiktok.com" not in url:
            await update.message.reply_text(
                "Kirim link TikTok yang valid."
            )
            return

        msg = await update.message.reply_text(
            "Sedang memproses video... ⏳"
        )

        # Nama file
        file_name = "video.mp4"

        # Setting yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': file_name,
            'noplaylist': True,
            'quiet': True,
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Kirim video
        with open(file_name, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption="Berhasil download ✅"
            )

        # Hapus pesan proses
        await msg.delete()

        # Hapus file setelah dikirim
        if os.path.exists(file_name):
            os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(
            f"Gagal download video.\n\nError:\n{e}"
        )

# Start bot
app = Application.builder().token(TOKEN).build()

# Handler pesan
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        download_tiktok
    )
)

print("Bot sedang berjalan...")

# Jalankan bot
app.run_polling()
