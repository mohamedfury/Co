import os
import json
from telebot.types import Message

DATA = "data"
MANAGERS_FILE = os.path.join(DATA, "managers.json")

def load_managers(chat_id):
    if not os.path.exists(MANAGERS_FILE):
        return []
    with open(MANAGERS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), [])

def save_managers(chat_id, managers):
    if not os.path.exists(MANAGERS_FILE):
        with open(MANAGERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(MANAGERS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = managers
    with open(MANAGERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(bot):

    @bot.message_handler(commands=['رفع_ادمن'])
    def add_manager(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "قم بالرد على رسالة العضو الذي تريد رفعه أدمن.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        managers = load_managers(chat_id)
        if user_id in managers:
            return bot.reply_to(message, "هذا العضو بالفعل أدمن.")
        managers.append(user_id)
        save_managers(chat_id, managers)
        bot.reply_to(message, "تم رفع العضو أدمن.")

    @bot.message_handler(commands=['تنزيل_ادمن'])
    def remove_manager(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "قم بالرد على رسالة العضو الذي تريد تنزيله من الأدمنية.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        managers = load_managers(chat_id)
        if user_id not in managers:
            return bot.reply_to(message, "هذا العضو ليس أدمن.")
        managers.remove(user_id)
        save_managers(chat_id, managers)
        bot.reply_to(message, "تم تنزيل العضو من الأدمنية.")

    @bot.message_handler(commands=['الادمنيه'])
    def list_managers(message: Message):
        chat_id = message.chat.id
        managers = load_managers(chat_id)
        if not managers:
            return bot.reply_to(message, "لا يوجد أدمنية في هذه المجموعة.")
        text = "📋 قائمة الأدمنية:\n"
        for user_id in managers:
            text += f"• `{user_id}`\n"
        bot.reply_to(message, text, parse_mode="Markdown")
