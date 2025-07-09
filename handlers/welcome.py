# handlers/welcome.py

import os
import json
from telebot.types import Message

DATA = "data"
WELCOME_FILE = os.path.join(DATA, "welcomes.json")
SETTINGS_FILE = os.path.join(DATA, "group_settings.json")

def load_welcome(chat_id):
    if not os.path.exists(WELCOME_FILE):
        return ""
    with open(WELCOME_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), "")

def save_welcome(chat_id, text):
    if not os.path.exists(WELCOME_FILE):
        with open(WELCOME_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(WELCOME_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = text
    with open(WELCOME_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_settings(chat_id):
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(chat_id), {})

def save_settings(chat_id, settings):
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(SETTINGS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data[str(chat_id)] = settings
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(bot):
    # تغيير رسالة الترحيب (بالرد)
    @bot.message_handler(commands=['ضع_ترحيب'])
    def set_welcome(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "رد على رسالة لتعيينها كرسالة الترحيب.")
        text = message.reply_to_message.text or ""
        save_welcome(message.chat.id, text)
        bot.reply_to(message, "تم حفظ رسالة الترحيب ✅")

    # عرض رسالة الترحيب الحالية
    @bot.message_handler(commands=['الترحيب'])
    def show_welcome(message: Message):
        text = load_welcome(message.chat.id)
        if text:
            bot.reply_to(message, f"رسالة الترحيب الحالية:\n{text}")
        else:
            bot.reply_to(message, "لا توجد رسالة ترحيب محددة لهذه المجموعة.")

    # تفعيل/تعطيل الترحيب
    @bot.message_handler(commands=['تفعيل_الترحيب', 'تعطيل_الترحيب'])
    def toggle_welcome(message: Message):
        settings = load_settings(message.chat.id)
        if 'تفعيل' in message.text:
            settings["welcome_on"] = True
            resp = "تم تفعيل الترحيب ✅"
        else:
            settings["welcome_on"] = False
            resp = "تم تعطيل الترحيب ❌"
        save_settings(message.chat.id, settings)
        bot.reply_to(message, resp)

    # إرسال الترحيب عند دخول عضو جديد
    @bot.message_handler(content_types=['new_chat_members'])
    def send_welcome(message: Message):
        settings = load_settings(message.chat.id)
        if not settings.get("welcome_on", True):
            return
        welcome_text = load_welcome(message.chat.id)
        if not welcome_text:
            welcome_text = "أهلاً وسهلاً بك في المجموعة!"
        for user in message.new_chat_members:
            bot.send_message(message.chat.id, welcome_text.replace("{العضو}", f"[{user.first_name}](tg://user?id={user.id})"), parse_mode="Markdown")
