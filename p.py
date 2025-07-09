import yt_dlp
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = '8073549221:AAErrZipsE_tePrgSg8AJMLTKyhS-pBtefA'  # Replace this with your actual bot token
CHANNEL_LINK = "https://t.me/+_ZyI9w3QwGU0ZTM1"  # Optional channel URL

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎬 **Welcome to InstaReel 4K Bot!**\n\nJust send me any public Instagram Reel link and I’ll give you the original high-quality video. 😍",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# About Button
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.edit_message_text(
            "🤖 *InstaReel 4K Downloader*\n\n📥 Downloads original reels in HD or 4K\n🚫 No watermark\n🔄 Powered by yt-dlp\n\n💡 Works only for public reels.",
            parse_mode="Markdown"
        )

# Reel Downloader
async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()

    if "instagram.com/reel/" not in link:
        await update.message.reply_text("❌ *Please send a valid Instagram Reel link.*", parse_mode="Markdown")
        return

    await update.message.reply_text("⏳ *Fetching video... Please wait...*", parse_mode="Markdown")

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloaded.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp4').replace('.mkv', '.mp4')

        with open(filename, 'rb') as video:
            keyboard = [[InlineKeyboardButton("🔄 Download Another", switch_inline_query_current_chat="")]]
            await update.message.reply_video(
                video=video,
                caption="✅ *Here's your reel in HD/4K!*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )

        os.remove(filename)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("⚠️ *Download failed.* The reel might be private or invalid.", parse_mode="Markdown")

# Run Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_reel))

    print("✅ Bot is running...")
    app.run_polling()
