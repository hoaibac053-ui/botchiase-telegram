from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import asyncio

TOKEN = "8571783970:AAH-yEE4Mc6sZMrOcNi-snEIcDx3uKmlFwY"  

# ID nhóm nguồn
SOURCE_CHAT_ID = -1002789303223

# Danh sách kênh đích
TARGET_CHANNELS = [
    -1003729153223,
    -1003538557311,
    -1003718790513
]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg or msg.chat_id != SOURCE_CHAT_ID:
        return

    for channel_id in TARGET_CHANNELS:
        try:
            await context.bot.forward_message(
                chat_id=channel_id,
                from_chat_id=SOURCE_CHAT_ID,
                message_id=msg.message_id
            )
            await asyncio.sleep(1)  # tránh spam
        except Exception as e:
            print(f"Lỗi gửi tới {channel_id}: {e}")



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

if __name__ == "__main__":
    print("Bot đang chạy...")
    app.run_polling()