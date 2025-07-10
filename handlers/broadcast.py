import os
import json
from telebot.types import Message

DATA = "data"
USERS_FILE = os.path.join(DATA, "users.json")

# تحميل معرفات المستخدمين
def load_all_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def get_all_user_ids():
    users = load_all_users()
    user_ids = set()
    for chat_data in users.values():
        user_ids.update(chat_data.keys())
    return list(user_ids)

def register(bot):
    # إذاعة عادية (نص فقط)
    @bot.message_handler(commands=["اذاعة"], func=lambda m: str(m.from_user.id) == str(bot.owner_id))
    def broadcast_text(message: Message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return bot.reply_to(message, "❗️ رد على رسالة نصية لإرسالها إذاعة.")
        user_ids = get_all_user_ids()
        count = 0
        for user_id in user_ids:
            try:
                bot.send_message(user_id, message.reply_to_message.text)
                count += 1
            except Exception:
                continue
        bot.reply_to(message, f"📢 تم إرسال الإذاعة إلى {count} مستخدم.")

    # إذاعة مرفقة بصورة
    @bot.message_handler(commands=["اذاعة_صورة"], func=lambda m: str(m.from_user.id) == str(bot.owner_id))
    def broadcast_photo(message: Message):
        if not message.reply_to_message or not message.reply_to_message.photo:
            return bot.reply_to(message, "❗️ رد على صورة لإرسالها إذاعة.")
        caption = message.reply_to_message.caption or ""
        user_ids = get_all_user_ids()
        count = 0
        for user_id in user_ids:
            try:
                bot.send_photo(user_id, message.reply_to_message.photo[-1].file_id, caption=caption)
                count += 1
            except Exception:
                continue
        bot.reply_to(message, f"📸 تم إرسال الإذاعة إلى {count} مستخدم.")
