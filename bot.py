from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import asyncio

TOKEN = "8571783970:AAH-yEE4Mc6sZMrOcNi-snEIcDx3uKmlFwY"

SOURCE_CHAT_ID = -1002789303223

TARGET_CHANNELS = [
    -1003729153223,
    -1003538557311,
    -1003718790513
]

media_groups = {}
media_tasks = {}

async def send_album(group_id, context):
    await asyncio.sleep(3)  # chờ gom đủ (quan trọng)

    if group_id not in media_groups:
        return

    msgs = media_groups[group_id]

    media = []
    caption_used = False

    for m in msgs:
        cap = ""
        if not caption_used and m.caption:
            cap = m.caption
            caption_used = True

        if m.photo:
            media.append(InputMediaPhoto(
                media=m.photo[-1].file_id,
                caption=cap
            ))

        elif m.video:
            media.append(InputMediaVideo(
                media=m.video.file_id,
                caption=cap
            ))

    # Telegram giới hạn tối đa 10 media / album
    media = media[:10]

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
    del media_tasks[group_id]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg or msg.chat_id != SOURCE_CHAT_ID:
        return

    #  ALBUM 
    if msg.media_group_id:
        group_id = msg.media_group_id

        if group_id not in media_groups:
            media_groups[group_id] = []

        media_groups[group_id].append(msg)

        # reset timer mỗi lần có media mới
        if group_id in media_tasks:
            media_tasks[group_id].cancel()

        media_tasks[group_id] = asyncio.create_task(
            send_album(group_id, context)
        )

        return

    for channel_id in TARGET_CHANNELS:
        try:
            if msg.text:
                await context.bot.send_message(
                    chat_id=channel_id,
                    text=msg.text
                )

            elif msg.photo:
                await context.bot.send_photo(
                    chat_id=channel_id,
                    photo=msg.photo[-1].file_id,
                    caption=msg.caption or ""
                )

            elif msg.video:
                await context.bot.send_video(
                    chat_id=channel_id,
                    video=msg.video.file_id,
                    caption=msg.caption or ""
                )

            elif msg.document:
                await context.bot.send_document(
                    chat_id=channel_id,
                    document=msg.document.file_id,
                    caption=msg.caption or ""
                )

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Lỗi gửi tới {channel_id}: {e}")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

if __name__ == "__main__":
    print("Bot đang chạy...")
    app.run_polling()