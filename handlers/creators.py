# handlers/creators.py

import os
import json
from telebot.types import Message

DATA = "data"
CREATORS_FILE = os.path.join(DATA, "creators.json")

def load_creators(chat_id):
    if not os.path.exists(CREATORS_FILE):
        return []
    with open(CREATORS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), [])

def save_creators(chat_id, creators):
    if not os.path.exists(CREATORS_FILE):
        with open(CREATORS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(CREATORS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = creators
    with open(CREATORS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_creator(chat_id, user_id):
    creators = load_creators(chat_id)
    if user_id not in creators:
        creators.append(user_id)
        save_creators(chat_id, creators)

def remove_creator(chat_id, user_id):
    creators = load_creators(chat_id)
    if user_id in creators:
        creators.remove(user_id)
        save_creators(chat_id, creators)

def clear_creators(chat_id):
    save_creators(chat_id, [])

def list_to_text(items, bot, chat_id):
    lines = []
    for uid in items:
        try:
            user = bot.get_chat_member(chat_id, uid).user
            lines.append(f"• [{user.first_name}](tg://user?id={uid})")
        except Exception:
            "\n".join(lines) if lines else "لا يوجد منشئين حالياً."

def register(bot):
    @bot.message_handler(commands=['رفع_منشئ'])
    def promote_creator(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لرفعه منشئ.")
        user_id = message.reply_to_message.from_user.id
        add_creator(message.chat.id, user_id)
        bot.reply_to(message, "تم رفع العضو منشئ ✅")

    @bot.message_handler(commands=['تنزيل_منشئ'])
    def demote_creator(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على العضو لتنزيله من المنشئين.")
        user_id = message.reply_to_message.from_user.id
        remove_creator(message.chat.id, user_id)
        bot.reply_to(message, "تم تنزيل العضو من المنشئين ✅")

    @bot.message_handler(commands=['المنشئين'])
    def show_creators(message: Message):
        creators = load_creators(message.chat.id)
        text = "قائمة المنشئين:\n" + list_to_text(creators, bot, message.chat.id)
        bot.reply_to(message, text, parse_mode="Markdown")

    @bot.message_handler(commands=['مسح_المنشئين'])
    def clear_all_creators(message: Message):
        clear_creators(message.chat.id)
        bot.reply_to(message, "تم مسح جميع المنشئين من المجموعة.")
