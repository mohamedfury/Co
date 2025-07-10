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

def register(bot):

    @bot.message_handler(commands=['رفع_منشئ'])
    def add_creator(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "قم بالرد على رسالة العضو الذي تريد رفعه منشئ.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        creators = load_creators(chat_id)
        if user_id in creators:
            return bot.reply_to(message, "هذا العضو بالفعل منشئ.")
        creators.append(user_id)
        save_creators(chat_id, creators)
        bot.reply_to(message, "تم رفع العضو منشئ.")

    @bot.message_handler(commands=['تنزيل_منشئ'])
    def remove_creator(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "قم بالرد على رسالة العضو الذي تريد تنزيله من المنشئين.")
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        creators = load_creators(chat_id)
        if user_id not in creators:
            return bot.reply_to(message, "هذا العضو ليس منشئ.")
        creators.remove(user_id)
        save_creators(chat_id, creators)
        bot.reply_to(message, "تم تنزيل العضو من المنشئين.")

    @bot.message_handler(commands=['المنشئين'])
    def list_creators(message: Message):
        chat_id = message.chat.id
        creators = load_creators(chat_id)
        if not creators:
            return bot.reply_to(message, "لا يوجد منشئين في هذه المجموعة.")
        text = "📋 قائمة المنشئين:\n"
        for user_id in creators:
            text += f"• `{user_id}`\n"
        bot.reply_to(message, text, parse_mode="Markdown")
