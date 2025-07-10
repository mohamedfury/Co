# handlers/managers.py

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

    @bot.message_handler(commands=["رفع_مدير"])
    def add_manager(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "📌 الرجاء الرد على رسالة المستخدم الذي تريد رفعه مدير.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        managers = load_managers(chat_id)
        if user_id in managers:
            return bot.reply_to(message, "⚠️ هذا المستخدم مدير بالفعل.")
        managers.append(user_id)
        save_managers(chat_id, managers)
        bot.reply_to(message, "✅ تم رفع المستخدم مدير.")

    @bot.message_handler(commands=["تنزيل_مدير"])
    def remove_manager(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "📌 الرجاء الرد على رسالة المستخدم الذي تريد تنزيله من المديرين.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        managers = load_managers(chat_id)
        if user_id not in managers:
            return bot.reply_to(message, "⚠️ هذا المستخدم ليس مدير.")
        managers.remove(user_id)
        save_managers(chat_id, managers)
        bot.reply_to(message, "✅ تم تنزيل المستخدم من المديرين.")

    @bot.message_handler(commands=["المديرين"])
    def list_managers(message: Message):
        chat_id = message.chat.id
        managers = load_managers(chat_id)
        if not managers:
            return bot.reply_to(message, "لا يوجد مديرين في هذه المجموعة.")
        text = "👥 قائمة المديرين:\n"
        for uid in managers:
            text += f"• [{uid}](tg://user?id={uid})\n"
        bot.reply_to(message, text, parse_mode="Markdown")

    @bot.message_handler(commands=["مسح_المديرين"])
    def clear_managers(message: Message):
        chat_id = message.chat.id
        save_managers(chat_id, [])
        bot.reply_to(message, "🗑 تم مسح جميع المديرين.")
