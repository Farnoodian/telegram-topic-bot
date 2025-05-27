from pyrogram import Client, filters
from pyrogram.types import Message

api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

app = Client("media_hub_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

topic_rules = {
    "انیمه | Anime": ["text", "video", "photo"],
    "فیلم و سریال | Movie & Series": ["text", "video", "photo"],
    "غذا | Food": ["text", "photo", "video"],
    "عکس | Photo": ["photo"],
    "متن | Text": ["text"],
    "موزیک | Music": ["audio", "voice", "document"],
    "ویدیو | Video": ["video"],
}

def get_message_type(message: Message):
    if message.audio or message.voice or message.document:
        return "audio"
    elif message.photo:
        return "photo"
    elif message.video:
        return "video"
    elif message.text:
        return "text"
    return "unknown"

@app.on_message(filters.group)
async def filter_topics(client, message: Message):
    if not message.is_topic_message:
        return

    topic_name = message.topic_name
    allowed_types = topic_rules.get(topic_name)
    if allowed_types is None:
        return

    content_type = get_message_type(message)
    if content_type not in allowed_types:
        await message.delete()
        await message.reply_text(
            f"❌ مجاز نیست! فقط موارد زیر در این تاپیک:\n{', '.join(allowed_types)}",
            quote=True
        )

app.run()
