from telegram import Update, InputMediaPhoto, InputMediaVideo
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

# Lưu album tạm
media_groups = {}

# Hàm xử lý tin nhắn
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg or msg.chat_id != SOURCE_CHAT_ID:
        return

    
    if msg.media_group_id:
        group_id = msg.media_group_id

        if group_id not in media_groups:
            media_groups[group_id] = []

        media_groups[group_id].append(msg)

        # chờ gom đủ album
        await asyncio.sleep(1.5)

        if len(media_groups[group_id]) > 1:
            media = []

            for m in media_groups[group_id]:
                if m.photo:
                    media.append(InputMediaPhoto(
                        media=m.photo[-1].file_id,
                        caption=m.caption if m.caption else ""
                    ))
                elif m.video:
                    media.append(InputMediaVideo(
                        media=m.video.file_id,
                        caption=m.caption if m.caption else ""
                    ))

            for channel_id in TARGET_CHANNELS:
                try:
                    await context.bot.send_media_group(
                        chat_id=channel_id,
                        media=media
                    )
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Lỗi album {channel_id}: {e}")

            del media_groups[group_id]

        return

    
    for channel_id in TARGET_CHANNELS:
        try:
            # TEXT
            if msg.text:
                await context.bot.send_message(
                    chat_id=channel_id,
                    text=msg.text
                )

            # ẢNH
            elif msg.photo:
                await context.bot.send_photo(
                    chat_id=channel_id,
                    photo=msg.photo[-1].file_id,
                    caption=msg.caption if msg.caption else ""
                )

            # VIDEO
            elif msg.video:
                await context.bot.send_video(
                    chat_id=channel_id,
                    video=msg.video.file_id,
                    caption=msg.caption if msg.caption else ""
                )

            # FILE
            elif msg.document:
                await context.bot.send_document(
                    chat_id=channel_id,
                    document=msg.document.file_id,
                    caption=msg.caption if msg.caption else ""
                )

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Lỗi gửi tới {channel_id}: {e}")



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

if __name__ == "__main__":
    print("Bot đang chạy...")
    app.run_polling()