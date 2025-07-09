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

def save_managers(chat_id managers:
        managers.append(user_id)
        save_managers(chat_id, managers)

def remove_manager(chat_id, user_id):
    managers = load_managers(chat_id)
    if user_id in managers:
        managers.remove(user_id)
        save_managers(chat_id, managers)

def clear_managers(chat_id):
    save_managers(chat_id, [])

def list_to_text(items, bot, chat_id):
    lines = []
    for uid in items:
        try:
            user = bot.get_chat_member(chat_id, uid).user
            lines.append(f"• [{user.first_name}](tg://user?id={uid})"• {uid}")
    return "\n".join(lines) if lines else "لا يوجد مدراء حالياً."

def register(bot):
    # رفع مدير
    @bot.message_handler(commands=['رفع_مدير'])
    def promote_manager(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لرفعه مدير.")
        user_id = message.reply_to_message.from_user.id
        add_manager(message.chat.id, user_id)
        bot.reply_to(message, "تم رفع العضو مدير ✅")

    # تنزيل مدير
    @bot.message_handler(commands=['تنزيل_مدير'])
    def demote_manager(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لتنزيله من المدراء.")
        user_id = message.reply_to_message.from_user.id
        remove_manager(message.chat.id, user_id)
        bot.reply_to(message, "تم تنزيل العضو من المدراء ✅")

    # عرض المدراء
    @bot.message_handler(commands=['المدراء'])
    def show_managers(message: Message):
        managers = load_managers(message.chat.id)
        text = "قائمة المدراء:\n" + list_to_text(managers, bot, message.chat.id)
        bot.reply_to(message, text, parse_mode="Markdown")

    # مسح المدراء
    @bot.message_handler(commands=['مسح_المدراء'])
    def clear_all_managers(message: Message):
        clear_managers(message.chat.id)
        bot.reply_to(message, "تم مسح جميع المدراء من المجموعة.")
