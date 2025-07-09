# handlers/broadcast.py

import os
import json
from telebot.types import Message

DATA = "data"
GROUPS_FILE = os.path.join(DATA, "groups.json")
USERS_FILE = os.path.join(DATA, "users.json")

def load_list(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

def save_list(filename, items):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def register(bot):
    # حفظ كل مجموعة جديدة يدخلها البوت
    @bot.message_handler(content_types=['new_chat_members'])
    def add_group(message: Message):
        groups = load_list(GROUPS_FILE)
        if message.chat.id not in groups:
            groups.append(message.chat.id)
            save_list(GROUPS_FILE, groups)

    # حفظ كل مستخدم خاص يستعمل البوت
    @bot.message_handler(content_types=['private'])
    def add_user(message: Message):
        users = load_list(USERS_FILE)
        if message.from_user.id not in users:
            users.append(message.from_user.id)
            save_list(USERS_FILE, users)

    # إذاعة للمجموعات (يرسل نص بالرد)
    @bot.message_handler(commands=['اذاعة_مجموعات'])
    def broadcast_groups(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على الرسالة التي تريد إذاعتها في كل المجموعات.")
        text = message.reply_to_message.text or ""
        groups = load_list(GROUPS_FILE)
        sent, failed = 0, 0
        for chat_id in groups:
            try:
                bot.send_message(chat_id, text)
                sent += 1
            except Exception:
                failed += 1
        bot.reply_to(message, f"تم إرسال الإذاعة إلى {sent} مجموعة.\nفشل الإرسال إلى {failed} مجموعة.")

    # إذاعة للمستخدمين (يرسل نص بالرد)
    @bot.message_handler(commands=['اذاعة_خاص'])
    def broadcast_users(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على الرسالة التي تريد إذاعتها لكل مستخدمي الخاص.")
        text = message.reply_to_message.text or ""
        users = load_list(USERS_FILE)
        sent, failed = 0, 0
        for user_id in users:
            try:
                bot.send_message(user_id, text)
                sent += 1
            except Exception:
                failed += 1
        bot.reply_to(message, f"تم إرسال الإذاعة إلى {sent} مستخدم.\nفشل الإرسال إلى {failed} مستخدم.")
