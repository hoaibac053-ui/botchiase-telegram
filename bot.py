from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import asyncio

TOKEN = "8571783970:AAH-yEE4Mc6sZMrOcNi-snEIcDx3uKmlFwY"

# ID nhóm riêng tư (nguồn)
SOURCE_CHAT_ID = -1002789303223

# Danh sách kênh phụ (đích)
TARGET_CHANNELS = [
    -1003729153223,
    -1003538557311,
    -1003718790513
]

# Hàm chỉnh sửa caption (tránh reup)
def edit_caption(text):
    if not text:
        return text

    text = text.replace("http", "hxxp")
    text += "\n\n👉 Tham gia kênh: @tenkenhcuaban"
    return text

# Xử lý tin nhắn
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.chat_id != SOURCE_CHAT_ID:
        return

    for channel_id in TARGET_CHANNELS:
        try:
            if msg.text:
                new_text = edit_caption(msg.text)
                await context.bot.send_message(
                    chat_id=channel_id,
                    text=new_text
                )

            elif msg.photo:
                caption = edit_caption(msg.caption)
                await context.bot.send_photo(
                    chat_id=channel_id,
                    photo=msg.photo[-1].file_id,
                    caption=caption
                )

            elif msg.video:
                caption = edit_caption(msg.caption)
                await context.bot.send_video(
                    chat_id=channel_id,
                    video=msg.video.file_id,
                    caption=caption
                )

            elif msg.document:
                caption = edit_caption(msg.caption)
                await context.bot.send_document(
                    chat_id=channel_id,
                    document=msg.document.file_id,
                    caption=caption
                )

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Lỗi gửi tới {channel_id}: {e}")

# Khởi chạy bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

if __name__ == "__main__":
    print("Bot đang chạy...")
    app.run_polling()