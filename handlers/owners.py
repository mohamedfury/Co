import os
import json
from telebot.types import Message

DATA = "data"
OWNERS_FILE = os.path.join(DATA, "owners.json")

def load_owners(chat_id):
    if not os.path.exists(OWNERS_FILE):
        return []
    with open(OWNERS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), [])

def save_owners(chat_id, owners):
    if not os.path.exists(OWNERS_FILE):
        with open(OWNERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(OWNERS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = owners
    with open(OWNERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(bot):

    @bot.message_handler(commands=['رفع_مالك'])
    def add_owner(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "قم بالرد على رسالة العضو الذي تريد رفعه مالك.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        owners = load_owners(chat_id)
        if user_id in owners:
            return bot.reply_to(message, "هذا العضو بالفعل مالك.")
        owners.append(user_id)
        save_owners(chat_id, owners)
        bot.reply_to(message, "تم رفع العضو مالك.")

    @bot.message_handler(commands=['تنزيل_مالك'])
    def remove_owner(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "قم بالرد على رسالة العضو الذي تريد تنزيله من المالكيـن.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        owners = load_owners(chat_id)
        if user_id not in owners:
            return bot.reply_to(message, "هذا العضو ليس مالكاً.")
        owners.remove(user_id)
        save_owners(chat_id, owners)
        bot.reply_to(message, "تم تنزيل العضو من المالكيـن.")

    @bot.message_handler(commands=['المالكيـن'])
    def list_owners(message: Message):
        chat_id = message.chat.id
        owners = load_owners(chat_id)
        if not owners:
            return bot.reply_to(message, "لا يوجد مالكيـن في هذه المجموعة.")
        text = "📋 قائمة المالكيـن:\n"
        for user_id in owners:
            text += f"• `{user_id}`\n"
        bot.reply_to(message, text, parse_mode="Markdown")
