import json
import os
from telebot.types import Message

DATA = "data"
USERS_FILE = os.path.join(DATA, "users.json")
ROLES_FILE = os.path.join(DATA, "roles.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_roles():
    if not os.path.exists(ROLES_FILE):
        return {}
    with open(ROLES_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def save_roles(data):
    with open(ROLES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def register(bot):

    @bot.message_handler(commands=['رتبتي'])
    def show_my_role(message: Message):
        roles = load_roles()
        role = roles.get(str(message.chat.id), {}).get(str(message.from_user.id), "عضو")
        bot.reply_to(message, f"رتبتك في هذه المجموعة: {role}")

    @bot.message_handler(commands=['رفع_رتبه'])
    def raise_role(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "❗️ الرجاء الرد على رسالة العضو لرفع رتبته.")
        roles = load_roles()
        chat_roles = roles.setdefault(str(message.chat.id), {})
        user_id = str(message.reply_to_message.from_user.id)
        chat_roles[user_id] = "مميز"
        save_roles(roles)
        bot.reply_to(message, f"✅ تم رفع رتبة العضو إلى مميز.")

    @bot.message_handler(commands=['تنزيل_رتبه'])
    def lower_role(message: Message):
        if not message.reply_to_message:
            return bot.reply_to(message, "❗️ الرجاء الرد على رسالة العضو لتنزيل رتبته.")
        roles = load_roles()
        chat_roles = roles.setdefault(str(message.chat.id), {})
        user_id = str(message.reply_to_message.from_user.id)
        chat_roles[user_id] = "عضو"
        save_roles(roles)
        bot.reply_to(message, f"✅ تم تنزيل رتبة العضو إلى عضو.")

    @bot.message_handler(commands=['قائمة_المميزين'])
    def list_special_members(message: Message):
        roles = load_roles()
        chat_roles = roles.get(str(message.chat.id), {})
        special_members = [uid for uid, role in chat_roles.items() if role == "مميز"]
        if not special_members:
            return bot.reply_to(message, "🚫 لا يوجد مميزين في هذه المجموعة.")
        text = "⭐️ قائمة المميزين:\n"
        for uid in special_members:
            text += f"• [{uid}](tg://user?id={uid})\n"
        bot.reply_to(message, text, parse_mode="Markdown")

    # يمكنك إضافة أوامر أخرى متعلقة بالأعضاء هنا
